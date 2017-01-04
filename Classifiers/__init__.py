from Classifiers.classifiers import *
from Utilities.orginizers import LearningData, DataAccessor, TrainingData
from sklearn.tree import DecisionTreeClassifier
import logging
import sklearn


def create_adaboost(data, classes,base_estimator=DecisionTreeClassifier()):
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