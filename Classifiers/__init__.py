from Classifiers.classifiers import *
from Utilities.orginizers import LearningData, DataAccessor
from sklearn.tree import DecisionTreeClassifier
import logging
import sklearn


def ready_training_data(stock_name, history_range=10, days_forward=1, change_threshold=0, startdate=None, enddate=None):
    ld = LearningData()
    data = ld.get_stock_data(stock_name, startdate=startdate, enddate=enddate)
    data = ld.add_history_fields(data, stock_name, history_range)
    length = len(data)
    data = data.dropna()
    if length - len(data) > 50:
        logging.warning("dropped more then {} samples containing not a number".format(length - len(data)))
    classes = ld.get_future_change_classification(data, stock_name, days_forward).apply(lambda x: x > change_threshold)
    return data, classes


def create_adaboost(stock_name=None, data=None, classes=None, days_forward=1, base_estimator=DecisionTreeClassifier()):
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