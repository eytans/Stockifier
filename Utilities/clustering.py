import pymongo
import sklearn.cluster
from Utilities import data_orginizers as do
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

def create_clustering_obj(start_date="1995-01-01",freq="BQ",stock_list=None,periods=(2016-1995)*4+3):
    """
    :param start_date:
    :param freq:
    :param stock_list:
    :param periods:
    :return:
    """
    ld = do.LearningData()
    if not stock_list:
        stock_list = ld.get_stock_names()
    clr = []   # array of k-means cluster
    stock_trend = dict.fromkeys(stock_list)  # dictionery in which the key is the ticker and the value is the stock trend data.
    date_array = pd.bdate_range(start=start_date, periods=periods,freq=freq)
    tickers = []
    data = []
    count = 0
    for st in stock_list:
        current_stock_data = ld.get_stock_data(st) #dataframe of the current stock
        # need to take in consideration case of "inf" in value
        value = current_stock_data.loc[date_array][['open', 'volume']].pct_change(1) # gets the open and volume of the current df and calculate the
                                                                                     # pct change
        value = value.fillna(value.mean()) # fill NaN with mean of the column
        value = value.replace('inf', 0.0)  # volume at the before exist is 0
        stock_trend[st] = value.values
        # tickers.addst the tags sould be the stock ticker
        data.append((list(itertools.chain.from_iterable(stock_trend[st]))))
        count += 1
    clustering = sklearn.cluster.KMeans()
    #print(len(data))
    clustering.fit(numpy.asarray(data))
    #TODO: the can't fit with the array of arrays need to some hoe convert it to Features*Samples matrix





# def get_relation_strength(stock,market,clustered_tree,precent=0.75):
#      market_stocks =
#      depth =

create_clustering_obj()



