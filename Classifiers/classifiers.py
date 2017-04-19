import sklearn.ensemble
import sklearn.cluster
import sklearn.metrics
from Utilities.orginizers import *
import Utilities
from math import *
import functools
import logging
import itertools
import collections
import numpy as np
from pathos import multiprocessing


# def split_quarters_by_cluster(df):
#     quarters = df.apply(lambda row: (row.name.month-1)//3, axis=1)
#     df['quarter'] = quarters
#     dfs = df.groupby('quarters')

class Quarter(object):
    def __init__(self, data: pd.DataFrame, cols=('open', 'volume'), name=''):
        self.reset(data, cols, name)

    def reset(self, data, cols=('open', 'volume'), name=''):
        drop_cols = list(data.columns)
        for c in cols:
            drop_cols.remove(c)
        self.data = data.drop(drop_cols, axis=1)
        self.start = self.data.iloc[0].name
        self.end = self.data.iloc[-1].name
        self.name = "{}-{}-{}".format(name, self.start, self.end)
        self.ready = False
        self.cluster = None

    def ready_quarter_data(self, minutes):
        if self.ready:
            return self
        self.data = TrainingData.cleanup_data(self.data, fill=False).astype(float)
        u = self.interpolate_extra_points(minutes)
        for c in u.columns:
            # times 1000 will later make the numerical error smaller (as now its with 0 error) but will not hurt
            # the distance outcome as it is proportional to the rest of the distances calculations. (because we are in
            # clustering it is ok).
            u[c] = 1000 * (u[c] / u[c].abs().sum())
        self.data = u
        self.ready = True
        return self

    def interpolate_extra_points(self, minutes: int):
        # Supposedly always includes original values because splitting by fraction of day
        indexes = pd.bdate_range(start=self.data.iloc[0].name, end=self.data.iloc[-1].name, freq="{}Min".format(minutes))
        res = self.data.reindex(indexes).interpolate(method='spline', order=3, s=0.)
        return res

    def __add__(self, other):
        # this is hacky and touching internals because its a project.
        # bad things: touch ready drop na setting index and moving dates
        if not self.ready:
            self.ready_quarter_data(24 * 60)

        if not other.ready:
            other.ready_quarter_data(24 * 60)

        mine_reindexed = self.data.set_index([list(range(self.data.shape[0]))]).fillna(0)
        other_reindexed = other.data.set_index([list(range(other.data.shape[0]))]).fillna(0)
        combined = (mine_reindexed + other_reindexed).fillna(0)

        index = self.data.index
        if combined.shape[0] > mine_reindexed.shape[0]:
            index = other.data.index
        res = Quarter(combined.set_index([index]))
        return res

    def __sub__(self, other):
        other_data = other.data * -1
        return self + Quarter(other_data)

    def __iadd__(self, other):
        res = (self+other).data
        self.reset(res, name=self.name)
        return self

    def __isub__(self, other):
        res = (self - other).data
        self.reset(res, name=self.name)
        return self

    def __truediv__(self, other):
        return self

    @staticmethod
    def split_by_quarters(stock_name: str, data: pd.DataFrame, cols=('open', 'volume')):
        # BQ is buisness quarter
        logging.debug("splitting {}".format(stock_name))
        splitters = pd.bdate_range(start=data.iloc[0].name, end=data.iloc[-1].name, freq="BQ")
        for start, end in Utilities.iterate_couples(splitters):
            temp = data[start:end]
            if start in temp.index and end in temp.index:
                del temp
                yield Quarter(data[start:end], name=stock_name, cols=cols)
        logging.debug("done {}".format(stock_name))


# What we need is a classifier which will receive a distance func which will work on one or more norms.
# in order to do that we need the data foreach quarter. This will be done in the following class which will let me
# split the data by quarters and interpolate extra points using spline (this is important to see behaviour).
# The classifier will be in Classifiers.
class QuarterDistance(object):
    def __init__(self, sampling_rate: int):
        """
        :param sampling_rate: how many samples to have per day.
        """
        self.ld = LearningData()
        self.minutes = int(60 * 24 / int(sampling_rate))

    def dist(self, u: Quarter, v: Quarter):
        """
        :param u: dataframe of quarter data (given by clustering algorithm). all quarters data should be normalized.
        :param v: same as u.
        :return: distance as measured by a few norms: float
        """
        u.ready_quarter_data(self.minutes)
        v.ready_quarter_data(self.minutes)

        u = u.data
        v = v.data

        total = sum(map(lambda c: self.l2_norm(u[c], v[c]), u.columns))
        total += sum(map(lambda c: self.lmax_norm(u[c], v[c]), u.columns))

        return total

    def l2_norm(self, u, v):
        total_d = 0.0
        for uval, vval in zip(u, v):
            total_d += (uval - vval) ** 2
        return sqrt(total_d)

    def lmax_norm(self, u, v):
        new = (u-v).apply(lambda x: fabs(x))
        res = new.max()
        return res


# Classifier implementing sklearn standards (for easier cross validation).
# This class creates 3 classifiers from the model, using the relation classifier if provided.
# relation classifier should have fields and strength for each connection
# classification is done using base estimator, strength*connections regularised by combined.
class ConnectionStrengthClassifier(sklearn.base.BaseEstimator):
    def __init__(self, threshold=0.1, base_strength=0.5, combined_weight=0.5, njobs=None, base_estimator=sklearn.tree.DecisionTreeClassifier()):
        """
        :param threshold: minimum value of relations to consider.
        :param combined_weight: the weight to put on the combined classifier.
        :param base_estimator: the estimator to use as a model for the fit.
        """
        self.base_estimator = base_estimator
        self.threshold = threshold
        self.combined_weight = combined_weight
        self.base_strength = base_strength
        self.njobs = njobs

    def fit(self, X, y, connection_columns, strengths):
        """
        :param X: data from which to learn
        :param y: classifications corresponding to @X
        :param connection_columns: a list of lists, each of which is the columns of a specific connection
        :param strengths: strength of a connection corresponding to @connection_columns
        :return: self after learning the given data
        """
        if X.shape[0] != y.shape[0]:
            raise ValueError("number of X rows must be equal to number of y rows.")
        used_cols = set(functools.reduce(lambda t, k: t+k, connection_columns))
        self.base_cols_ = [c for c in X.columns if c not in used_cols]
        self.base_estimator_ = sklearn.base.clone(self.base_estimator).fit(X[self.base_cols_], y)

        self.combined_estimators_ = []
        self.connections_estimators_ = []
        self.relations_ = []
        self.cols_ = []
        pool = multiprocessing.Pool(processes=self.njobs)

        for cols, stren in zip(connection_columns, strengths):
            if stren < self.threshold:
                continue
            cols = [c for c in cols if c in X.columns]
            if len(cols) == 0:
                continue
            self.relations_.append(stren)
            self.cols_.append(cols)

        def train_connection(cols):
            return sklearn.base.clone(self.base_estimator).fit(X[cols], y)

        self.connections_estimators_ = list(pool.map(train_connection, self.cols_))

        def train_combined(cols):
            return sklearn.base.clone(self.base_estimator).fit(X[self.base_cols_ + cols], y)

        self.combined_estimators_ = list(pool.map(train_combined, self.cols_))

        self.classes_ = self.base_estimator_.classes_
        pool.close()
        return self

    def __predict_from_probs(self, probs):
        bp = 0
        bi = 0
        for i, p in enumerate(probs):
            if bp < p:
                bp, bi = p, i
        return self.classes_[bi]

    def predict(self, X):
        predictions = self.predict_proba(X)
        return [self.__predict_from_probs(probs) for probs in predictions]

    def predict_proba(self, X):
        predictions = []
        for combined_e, connection_e, cols in zip(self.combined_estimators_, self.connections_estimators_, self.cols_):
            combined = combined_e.predict_proba(X[self.base_cols_ + cols])
            connect = connection_e.predict_proba(X[cols])
            predictions.append((combined * self.combined_weight) + ((1 - self.combined_weight) * connect))

        # used to be maximum of self.relations_ and 1 we want to test self.realtions_
        base = [self.base_strength * p for p in self.base_estimator_.predict_proba(X[self.base_cols_])]
        results = []
        for rel, probs in zip(self.relations_, predictions):
            results.append([b + p * rel for b, p in zip(base, probs)])
        return functools.reduce(lambda x, y: [x1 + y1 for x1, y1 in zip(x, y)], results)

    def score(self, X, y):
        return sklearn.metrics.accuracy_score(y, self.predict(X))


class Quarterizer(sklearn.base.BaseEstimator):
    def __init__(self, cols=('open', 'volume')):
        self.cols = cols
        self.length_ = 0
        self.distance_ = QuarterDistance(4)

    def fit(self, X: pd.DataFrame):
        if (not isinstance(X.index, pd.DatetimeIndex) and not isinstance(X.index, pd.TimedeltaIndex) and
                not isinstance(X.index, pd.PeriodIndex)):
            raise RuntimeError("Quartariser data must be indexed by date")

        X = self.to_quarters(X)

        self.length_ = min(map(lambda q: q.data.shape[0], X))
        return self

    def to_quarters(self, X: pd.DataFrame):
        for c in X.columns:
            if c not in self.cols:
                X.drop(c, axis=1)
        quarters = list(Quarter.split_by_quarters('', X, cols=self.cols))

        def no_col_empty(q: Quarter):
            for col in q.data.columns:
                if q.data[col].isnull().sum() == len(q.data):
                    return False
            return True

        data_it = map(lambda q: q.ready_quarter_data(self.distance_.minutes), quarters)
        X = list(filter(no_col_empty, data_it))
        return X

    def transform(self, X: pd.DataFrame):
        data = []
        for q in self.to_quarters(X):
            if len(q.data) > self.length_:
                q = Quarter(q.data.iloc[0:self.length_])
            if len(q.data) < self.length_:
                d = q.data
                d = d.resample('{}M'.format(self.distance_.minutes), periods=self.length_)
                q = Quarter(d)
                q.ready_quarter_data(self.distance_.minutes)
            data.append(q)

        starts = [q.start for q in data]
        ends = [q.end for q in data]
        data = [np.concatenate([q.data[c].values for c in q.data.columns]) for q in data]
        data = pd.DataFrame.from_records(data)
        data['start'] = starts
        data['end'] = ends
        return data

    @staticmethod
    def cut_by_classes(original_data, q_data, classes):
        """
        :param original_data: Data from which quarters were made
        :param q_data: Data after transform
        :param classes: the classes for q_data
        :return: dictionary of class to dataframe made from original data
        """
        if not isinstance(classes, pd.Series):
            classes = pd.Series(classes)

        res = collections.defaultdict(lambda: pd.DataFrame())
        for q_row, c_row in zip(q_data.iterrows(), classes.iteritems()):
            q_row = q_row[1]
            c_row = c_row[1]
            res[c_row] = pd.concat([res[c_row], original_data.loc[q_row['start']:q_row['end']]])

        return res

