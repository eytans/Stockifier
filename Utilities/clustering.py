import sklearn.cluster
from Utilities.orginizers import LearningData
import pandas as pd
import itertools
import numpy


def find_maximal_for_stock_and_market(self, path_to_stock,path_to_market):
    first,last = self.maximal_shared_range_dir(path_to_market)
    stock_file = open(path_to_stock,'r')
    list_of_all_dates = []
    for line in stock_file.readlines():
        list_of_all_dates.append(line.split(',')[1])
    if first < self.getdate(list_of_all_dates[0]):
        first = self.getdate(list_of_all_dates[0])
    if last > self.getdate(list_of_all_dates[len(list_of_all_dates)-1]):
        last = self.getdate(list_of_all_dates[len(list_of_all_dates)-1])
    return first, last


def find_smallest_common(self,s1,s2):
    """
    This function excepts two stocks and returns how up you need to go in the tree in order for the stocks to
    be at the same cluster
    :return:
    """


def create_clustering_obj(start_date="1995-01-01", stock_list=None, freq="BQ", periods=(2016-1995)*4+3):
    """
    :param start_date:
    :param stock_list:
    :param freq: see pandas.bdate_range
    :param periods: see pandas.bdate_range
    :return:
    """
    ld = LearningData()
    if not stock_list:
        stock_list = ld.get_stock_names()
    clr = []   # array of k-means cluster

    # dictionery in which the key is the ticker and the value is the stock trend data.
    stock_trend = dict.fromkeys(stock_list)
    date_array = pd.bdate_range(start=start_date, periods=periods, freq=freq)
    data = []
    for st in stock_list:
        current_stock_data = ld.get_stock_data(st)
        # need to take in consideration case of "inf" in value

        # gets the open and volume of the current df and calculate the precentage of change
        value = current_stock_data.loc[date_array][['open', 'volume']].pct_change(1)
        # fill NaN with mean of the column
        value = value.fillna(value.mean())
        # volume at the before exist is 0
        value = value.replace('inf', 0.0)
        stock_trend[st] = value
        # need to take the two columns and create a feature row from it. (single row for cluster)
        # we have 2 columns, open and volume and many dates.

        data.append(stock_trend[st]['volume'].append(stock_trend[st]['open'], ignore_index=True))
        # data.append((list(itertools.chain.from_iterable(stock_trend[st]))))
    clustering = sklearn.cluster.KMeans()
    clustering.fit(data)
    #TODO: the can't fit with the array of arrays need to some hoe convert it to Features*Samples matrix





# def get_relation_strength(stock,market,clustered_tree,precent=0.75):
#      market_stocks =
#      depth =

create_clustering_obj()



