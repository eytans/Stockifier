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
    data = [val for val in filter(lambda x: end >= x >= start, retreive_daily_markets_data())]
    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)


def train_stock(stock_data):
    data, results = get_data_and_results_from_stock(stock_data)
    return __get_general_classifier(data, results)
