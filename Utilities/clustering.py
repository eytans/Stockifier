import pymongo
import sklearn.cluster
from Utilities import data_orginizers as do
import pandas as pd


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
    :param ld: learning data class
    :param start_date:
    :param end_date:
    :param stock_list:
    :return:  array of k-mean clustering objects that cluster according to
    """
    ld = do.LearningData()
    if not stock_list:
        stock_list = ld.get_stock_names()
    clr = []   # array of k-means cluster
    stock_trend = dict.fromkeys(stock_list)  # dictionery in which the key is the ticker and the value is the stock trend data.
    date_array = pd.bdate_range(start=start_date, periods=periods,freq=freq)
    for st in stock_list:
        current_stock_data = ld.get_stock_data(st)
        # need to take in consideration case of "inf" in value
        value = current_stock_data.loc[date_array][['open', 'volume']].pct_change(1)
        value = value.fillna(value.mean())
        value = value.replace('inf', 0.0)  # volume at the before exist is 0
        stock_trend[st] = value.values
    tmp = sklearn.cluster.KMeans()
    tmp.fit([stock_trend["ABC"]])
    print()



# def get_relation_strength(stock,market,clustered_tree,precent=0.75):
#      market_stocks =
#      depth =

create_clustering_obj()



