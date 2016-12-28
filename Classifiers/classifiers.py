import sklearn.ensemble
from sklearn.tree import DecisionTreeClassifier
import sklearn.cluster
from Utilities.orginizers import *
import Utilities
from math import *
import logging


def apply_func(func, iterable):
    for i in iterable:
        func(i)
        yield i


def ready_training_data(stock_name, days_forward=1, change_threshold=0, startdate=None, enddate=None):
    ld = LearningData()
    data = ld.get_stock_data(stock_name, startdate=startdate, enddate=enddate)
    data = ld.add_history_fields(data, stock_name, 10)
    length = len(data)
    data = data.dropna()
    if length - len(data) > 50:
        logging.warning("dropped more then 50 samples containing not a number")
    classes = ld.get_future_change_classification(data, stock_name, days_forward).apply(lambda x: x > change_threshold)
    return data, classes


def create_adaboost(stock_name=None, data=None, classes=None, days_forward=1, base_estimator=DecisionTreeClassifier):
    if (data is None or classes is None) and stock_name is None:
        raise ValueError("Need at least stock_name or data+classes")
    if data is None or classes is None:
        data, classes = ready_training_data(stock_name, days_forward=days_forward)
    res = sklearn.ensemble.AdaBoostClassifier(base_estimator=base_estimator, n_estimators=200).fit(data, classes)
    return res


def create_quarter_clusterer(ld: LearningData, stock_names=None):
    if not stock_names:
        stock_names = ld.get_stock_names()
    quarters = DataAccessor(DataAccessor.Names.quarter)
    drop_cols = list(ld.get_stock_data(stock_names[0]).columns)
    drop_cols.remove('open')
    drop_cols.remove('volume')
    stocks_data = [(s, ld.get_stock_data(s).drop(drop_cols, axis=1)) for s in stock_names]
    full_data = []
    for s_name, d in stocks_data:
        if s_name not in quarters:
            quarters[s_name] = list(Quarter.split_by_quarters(s_name, d))
        full_data.extend(quarters[s_name])

    distance_object = QuarterDistance(4)
    for q in full_data:
        q.ready_quarter_data(distance_object.minutes)

    shortest = min(map(lambda q: q.data.shape[0], full_data))
    def arrange_data_frame(data: pd.DataFrame, len: int):
        res = None
        data = data.iloc[0:len]
        for c in data.columns:
            if res is None:
                res = data[c]
                continue
            res = res.append(data[c])
        return res

    full_data = [arrange_data_frame(q.data, shortest) for q in full_data]
    # clusterer = KMeansClusterer(num_means=6, distance=distance_object.dist, repeats=25, avoid_empty_clusters=True)
    # results = clusterer.cluster(vectors=full_data)
    clusterer = sklearn.cluster.KMeans().fit(full_data)
    return clusterer


# def split_quarters_by_cluster(df):
#     quarters = df.apply(lambda row: (row.name.month-1)//3, axis=1)
#     df['quarter'] = quarters
#     dfs = df.groupby('quarters')

class Quarter(object):
    def __init__(self, data: pd.DataFrame, cols=('open', 'volume'), name=''):
        self.reset(data, cols)

    def reset(self, data, cols=('open', 'volume'), name=''):
        drop_cols = list(data.columns)
        for c in cols:
            drop_cols.remove(c)
        self.name = name
        self.data = data.drop(drop_cols, axis=1)
        self.start = self.data.iloc[0].name
        self.end = self.data.iloc[-1].name
        self.ready = False
        self.cluster = None

    def ready_quarter_data(self, minutes):
        if self.ready:
            return
        u = self.interpolate_extra_points(minutes)
        for c in u.columns:
            # times 1000 will later make the numerical error smaller (as now its with 0 error) but will not hurt
            # the distance outcome as it is proportional to the rest of the distances calculations. (because we are in
            # clustering it is ok).
            u[c] = 1000 * (u[c] / u[c].abs().sum())
        self.data = u
        self.ready = True

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
    def split_by_quarters(stock_name: str, data: pd.DataFrame):
        # BQ is buisness quarter
        logging.debug("splitting {}".format(stock_name))
        splitters = pd.bdate_range(start=data.iloc[0].name, end=data.iloc[-1].name, freq="BQ")
        for start, end in Utilities.iterate_couples(splitters):
            temp = data[start:end]
            if start in temp.index and end in temp.index:
                del temp
                yield Quarter(data[start:end], name=stock_name)
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
