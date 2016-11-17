import sklearn.ensemble
from itertools import tee
from collections import OrderedDict


def __get_general_classifier(data, classes):
    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)


def apply_func(func, iterable):
    for i in iterable:
        func(i)
        yield i


def get_data_and_results_from_stock(stock_data):
    data = list(map(lambda d: OrderedDict(sorted(d.items())), stock_data))
    data.sort(key=lambda r: r['intdate'])
    data = list(data)
    results = list(map(lambda d: (d['close'] - d['open']) * d['open'] < 0.3, data[1:]))
    data = list(map(lambda d: list(d.values()), data))
    data = data[:-1]
    return data, results


def train_stock(stock_data):
    data, results = get_data_and_results_from_stock(stock_data)
    return __get_general_classifier(data, results)
