from Utilities.data_orginizers import *
import sklearn.ensemble


def get_general_classifier(data, classes):
    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)


def get_by_market_classifier(markets_dict, classes, start, end):
    data = [val for key, val in filter(lambda x: end >= x >= start, markets_dict.items())]
    data.sort(key=lambda l: l[0]['intdate'])
    market_name_sorter = dictionary_sorter(data[0])
    data = [market_name_sorter(d) for d in data]
    market_data_sorter = dictionary_sorter(data[0][0])
    data = [[market_data_sorter(m) for m in day] for day in data]

    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)


def get_per_market_classifier(markets_dict, stock_data, classes):
    pass