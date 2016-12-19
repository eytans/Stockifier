import sklearn.ensemble
from Utilities.orginizers import *


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


def split_quarters_by_cluster(df):
    quarters = df.apply(lambda row: (row.name.month-1)//3, axis=1)
    df['quarter'] = quarters
    dfs = df.groupby('quarters')

