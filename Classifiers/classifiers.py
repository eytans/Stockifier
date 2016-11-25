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

def get_by_market_classifier(markets_dict, classes, start, end):
    data = [val for key, val in filter(lambda x: end >= x >= start, markets_dict.items())]
    data.sort(key=lambda l: l[0]['intdate'])
    market_name_sorter = dictionary_sorter(data[0])
    data = [market_name_sorter(d) for d in data]
    market_data_sorter = dictionary_sorter(data[0][0])
    data = [[market_data_sorter(m) for m in day] for day in data]

    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)

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
