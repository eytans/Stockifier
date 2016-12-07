import pymongo
import pickle
import os
import pandas as pd
import Utilities


class LearningData(object):
    # save data as database to names to pandas.DataFrames
    __market_data = {}
    __stock_data = {}

    class DictionarySorter(object):
        '''Using a sample dictionary create a fast mapping from key to index.
        API include way to get a key for a given index and to create a list from a different dictionary with same keys.
        '''
        def __init__(self, sample):
            keys = list(sample.keys())
            keys.sort()
            self.sorting_dict = {key: i for i, key in enumerate(keys)}

        def __call__(self, d, *args, **kwargs):
            vals = [0] * len(self.sorting_dict)
            for k in d.keys():
                vals[self.sorting_dict[k]] = d[k]
            return vals

        def sort(self, d):
            return self(d)

        def get_index(self, key):
            return self[key]

        def __getitem__(self, item):
            return self.sorting_dict[item]

    def __init__(self, database='exchange', legal_markets=None):
        self.client = pymongo.MongoClient()
        db = self.client[database]
        self.database = database
        self.markets = db['markets']
        self.stocks = db['stocks']
        self.legal_markets = legal_markets
        if self.legal_markets is None:
            self.legal_markets = self.markets.distinct('market_name')

        self.market_sorter = LearningData.DictionarySorter(self.markets.find_one())
        self.stock_sorter = LearningData.DictionarySorter(self.stocks.find_one())

    def __init_market_data(self, market_name=None):
        if self.database not in LearningData.__market_data:
            LearningData.__market_data[self.database] = {}
        data = LearningData.__market_data[self.database]
        if market_name:
            if market_name not in data:
                query = {'market_name': market_name}
                data[market_name] = pd.DataFrame(list(self.markets.find(query)))
        else:
            for m in self.markets.distinct('market_name'):
                if m in data:
                    continue
                query = {'market_name': m}
                data[m] = pd.DataFrame(list(self.markets.find(query)))

    @classmethod
    def save(cls, path=None):
        if not path:
            path = Utilities.default_pickle
        data = (cls.__market_data, cls.__stock_data)
        pickle.dump(data, path)

    @classmethod
    def load(cls, path=None):
        if not os.path.exists(path):
            return
        cls.__market_data, cls.__stock_data = pickle.load(path)

    def get_market_data(self, market_name=None, startdate=None, enddate=None):
        self.__init_market_data(market_name)
        if not market_name:
            df = LearningData.__market_data[self.database]
        else:
            df = LearningData.__market_data[self.database][market_name]
        return self.slice_by_date(df, enddate, startdate)

    def slice_by_date(self, df, enddate, startdate):
        if startdate and not enddate:
            return df[df.date > startdate]
        if enddate and not startdate:
            return df[df.date < enddate]
        else:
            return df[df.date < enddate, df.date > startdate]

    def __init_stock_data(self, stock_name=None):
        if self.database not in LearningData.__stock_data:
            LearningData.__stock_data[self.database] = {}
        data = LearningData.__stock_data[self.database]
        if stock_name:
            if stock_name not in data[self.database]:
                query = {'ticker': stock_name}
                data[stock_name] = pd.DataFrame(list(self.stocks.find(query)))
        else:
            for doc in self.stocks.distinct('ticker'):
                name = doc['ticker']
                if name not in data:
                    query = {'ticker': name}
                    data[name] = pd.DataFrame(list(self.stocks.find(query)))

    def get_stock_data(self, stock_name=None, startdate=None, enddate=None):
        self.__init_stock_data(stock_name)
        if not stock_name:
            df = LearningData.__stock_data[self.database]
        else:
            df = LearningData.__stock_data[self.database][stock_name]
        return self.slice_by_date(df, enddate, startdate)
