import sklearn.ensemble
from itertools import tee
from collections import OrderedDict
from Utilities.data_orginizers import *


def get_general_classifier(data, classes):
    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)


def apply_func(func, iterable):
    for i in iterable:
        func(i)
        yield i


def get_by_market_classifier(classes, start, end):
    ld = LearningData()
    data = [val for val in filter(lambda x: end >= x >= start, ld.retreive_daily_markets_data())]
    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)


def train_stock(stock_data):
    ld = LearningData()
    data, results = ld.get_data_and_results_from_stock(stock_data)
    return get_general_classifier(data, results)
