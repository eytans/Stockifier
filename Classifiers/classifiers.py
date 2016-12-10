import sklearn.ensemble
from itertools import islice
from Utilities.data_orginizers import *
import Utilities


def get_general_classifier(data, classes):
    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)


def apply_func(func, iterable):
    for i in iterable:
        func(i)
        yield i


def get_float_change(df, days_forward):
    return [row['close'] - row[Utilities.stock_history_field(days_forward)]
            for row in islice(df.iterrows(), days_forward, None)] + [0]*days_forward


def ada_boosted_by_change(days):
    ld = LearningData()
    df = ld.flat_pointers(ld.get_stock_data('ABC'), 10)
    classes = get_float_change(df, days)
    return get_general_classifier(df, classes)


