import sklearn.ensemble
from nltk.cluster.kmeans import KMeansClusterer
from Utilities.orginizers import *
import Utilities
from math import *
import logging


def get_general_classifier(data, classes):
    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)


def apply_func(func, iterable):
    for i in iterable:
        func(i)
        yield i


def create_quarter_clusterer(ld: LearningData):
    stock_names = ld.get_stock_names()
    drop_cols = list(ld.get_stock_data(stock_names[0]).columns)
    drop_cols.remove('open')
    drop_cols.remove('volume')
    stocks_data = [(s, ld.get_stock_data(s).drop(drop_cols, axis=1)) for s in stock_names]
    full_data = []
    for s_name, d in stocks_data:
        full_data.extend(list(Quarter.split_by_quarters(s_name, d)))
    distance_object = QuarterDistance(4)
    clusterer = KMeansClusterer(num_means=8, distance=distance_object.dist, repeats=25)
    return clusterer


# def split_quarters_by_cluster(df):
#     quarters = df.apply(lambda row: (row.name.month-1)//3, axis=1)
#     df['quarter'] = quarters
#     dfs = df.groupby('quarters')

class Quarter(object):
    def __init__(self, stock_name: str, data: pd.DataFrame, cols=('open', 'volume')):
        self.name = stock_name
        drop_cols = list(data.columns)
        for c in cols:
            drop_cols.remove(c)
        self.data = data.drop(drop_cols)
        try:
            self.start = self.data.iloc[0]
        except:
            pass
        self.end = self.data.iloc[-1]
        self.ready = False

    def ready_quarter_data(self, minutes):
        if self.ready:
            return
        u = self.interpolate_extra_points(minutes)
        col_to_data = {col: u[col].values for col in u.columns}
        u = pd.DataFrame(col_to_data, index=range(u.shape[0]))
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

    @staticmethod
    def split_by_quarters(stock_name: str, data: pd.DataFrame):
        # BQ is buisness quarter
        logging.debug("splitting {}".format(stock_name))
        splitters = pd.bdate_range(start=data.iloc[0].name, end=data.iloc[-1].name, freq="BQ")
        for start, end in Utilities.iterate_couples(splitters):
            temp = data[start:end]
            if start in temp.index and end in temp.index:
                del temp
                yield Quarter(stock_name, data[start:end])
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
