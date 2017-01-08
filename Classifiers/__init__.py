from Classifiers.classifiers import *
from Utilities.orginizers import LearningData, DataAccessor, TrainingData
from sklearn.tree import DecisionTreeClassifier
import logging
import sklearn
import itertools


def create_adaboost(data, classes, base_estimator=DecisionTreeClassifier()):
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

        full_data = itertools.chain(full_data, quarters[s_name])

    distance_object = QuarterDistance(4)

    def no_col_empty(q: Quarter):
        for col in q.data.columns:
            if q.data[col].isnull().sum() == len(q.data):
                return False
        return True

    data_it = map(lambda q: q.ready_quarter_data(distance_object.minutes), full_data)
    full_data = list(filter(no_col_empty, data_it))

    shortest = min(map(lambda q: q.data.shape[0], full_data))

    def arrange_data_frame(data: pd.DataFrame, length: int):
        res = None
        data = data.iloc[0:length]

        for i, c in enumerate(data.columns):
            cur = data[c]
            cur.index = list(range(i*length, (i+1)*length))
            if res is None:
                res = cur
                continue
            res = res.append(cur)
        return res

    full_data = [arrange_data_frame(q.data, shortest) for q in full_data]
    clusterer = sklearn.cluster.KMeans().fit(full_data)
    return clusterer