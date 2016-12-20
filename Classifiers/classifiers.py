import sklearn.ensemble
from Utilities.orginizers import *
import Utilities
from math import *
from collections import defaultdict
import typing


def get_general_classifier(data, classes):
    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)


def apply_func(func, iterable):
    for i in iterable:
        func(i)
        yield i


def ada_boosted_by_change(days):
    ld = LearningData()
    stock_name = 'ABC'
    df = ld.add_history_fields(ld.get_stock_data(stock_name), 10)
    classes = ld.get_future_change_classification(df, stock_name, days)
    return get_general_classifier(df, classes)


# def split_quarters_by_cluster(df):
#     quarters = df.apply(lambda row: (row.name.month-1)//3, axis=1)
#     df['quarter'] = quarters
#     dfs = df.groupby('quarters')


# What we need is a classifier which will receive a distance func which will work on one or more norms.
# in order to do that we need the data foreach quarter. This will be done in the following class which will 8let me
# split the data by quarters and interpolate extra points using spline (this is important to see behaviour).
# The classifier will be in Classifiers.
class QuarterDistance(object):
    def __init__(self, sampling_rate: int):
        """
        :param sampling_rate: how many samples to have per day.
        """
        self.ld = LearningData
        self.minutes = int(60 * 24 / int(sampling_rate))

    @staticmethod
    def split_by_quarters(data):
        # BQ is buisness quarter
        splitters = pd.bdate_range(start=data.iloc[0].name, end=data.iloc[-1].name, freq="BQ")
        for start, end in Utilities.iterate_couples(splitters):
            yield data[start:end]

    def interpolate_extra_points(self, data: pd.DataFrame):
        # Supposedly always includes original values because splitting by fraction of day
        indexes = pd.bdate_range(start=data.iloc[0].name, end=data.iloc[-1].name, freq="{}Min".format(self.minutes))
        res = data.reindex(indexes).interpolate(method='spline', order=3, s=0.)
        return res

    def dist(self, u: pd.DataFrame, v: pd.DataFrame):
        """
        :param u: dataframe of quarter data (given by clustering algorithm). all quarters data should be normalized.
        :param v: same as u.
        :return: distance as measured by a few norms: float
        """

        u = self.ready_quarter_data(u)
        v = self.ready_quarter_data(v)

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

    def ready_quarter_data(self, u):
        u = self.interpolate_extra_points(u)
        col_to_data = {col: u[col].values for col in u.columns}
        u = pd.DataFrame(col_to_data, index=range(u.shape[0]))
        for c in u.columns:
            # times 1000 will later make the numerical error smaller (as now its with 0 error) but will not hurt
            # the distance outcome as it is proportional to the rest of the distances calculations. (because we are in
            # clustering it is ok).
            u[c] = 1000 * (u[c] / u[c].sum())
        return u
