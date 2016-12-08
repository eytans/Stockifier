import pymongo
import pickle
import os
import pandas as pd
import Utilities


class LearningData(object):
    # save data as database to names to pandas.DataFrames
    _market_data = {}
    _stock_data = {}

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

    def __init_market_data(self, market_name=None, force=False):
        if self.database not in LearningData._market_data:
            LearningData._market_data[self.database] = {}
        data = LearningData._market_data[self.database]
        if market_name:
            if market_name not in data or force:
                query = {'market_name': market_name}
                data[market_name] = pd.DataFrame(list(self.markets.find(query))).set_index(['date'])
        else:
            for m in self.markets.distinct('market_name'):
                if m in data and not force:
                    continue
                query = {'market_name': m}
                data[m] = pd.DataFrame(list(self.markets.find(query))).set_index(['date'])

    def __init_stock_data(self, stock_name=None, force=False):
        if self.database not in LearningData._stock_data:
            LearningData._stock_data[self.database] = {}
        data = LearningData._stock_data[self.database]
        if stock_name:
            if stock_name not in data or force:
                query = {'ticker': stock_name}
                data[stock_name] = pd.DataFrame(list(self.stocks.find(query))).set_index(['date'])
        else:
            for name in self.stocks.distinct('ticker'):
                if name not in data or force:
                    query = {'ticker': name}
                    data[name] = pd.DataFrame(list(self.stocks.find(query))).set_index(['date'])

    @classmethod
    def save(cls, path=None):
        if not path:
            path = Utilities.default_pickle
        data = (cls._market_data, cls._stock_data)
        with open(path, 'wb') as out:
            pickle.dump(data, out)

    @classmethod
    def load(cls, path=None):
        if not os.path.exists(path):
            return
        with open(path, 'rb') as data:
            cls._market_data, cls._stock_data = pickle.load(data)

    def get_market_data(self, market_name=None, startdate=None, enddate=None, force=False):
        self.__init_market_data(market_name, force)
        if not market_name:
            df = LearningData._market_data[self.database]
        else:
            df = LearningData._market_data[self.database][market_name]
        return self.slice_by_date(df, startdate, enddate)

    @staticmethod
    def slice_by_date(df, startdate, enddate):
        if startdate and not enddate:
            return df[startdate:]
        if enddate and not startdate:
            return df[:enddate]
        elif enddate and startdate:
            return df[startdate:enddate]
        else:
            return df.copy(False)

    def get_stock_data(self, stock_name=None, startdate=None, enddate=None, force=False):
        self.__init_stock_data(stock_name, force)
        if not stock_name:
            df = LearningData._stock_data[self.database]
        else:
            df = LearningData._stock_data[self.database][stock_name]
        return self.slice_by_date(df, startdate, enddate)

    def flat_pointers(self, df, stock_range, market_range=None, legal_markets=None):
        if not market_range:
            market_range = stock_range
        # TODO: less hacky range
        all_stock_history_fields = [Utilities.stock_history_field(i) for i in range(1, stock_range + 10000)]
        all_market_history_fields = [Utilities.market_history_field(i) for i in range(1, market_range + 10000)]
        bad_stock_names = set(all_stock_history_fields[stock_range:])
        bad_market_names = set(all_market_history_fields[market_range:])
        stock_drop_columns = [c for c in df.columns if c in bad_stock_names]
        market_drop_columns = [c for c in df.columns if c in bad_market_names]
        # drops all columns which shouldn't be here (all the names gathered)
        df.drop(stock_drop_columns + market_drop_columns, axis=1, inplace=True)

        # now for all fields that weren't dropped start creating a ton of features
        all_stock_history_fields = set(all_stock_history_fields)
        all_market_history_fields = set(all_market_history_fields)
        for c in df.columns:
            if c in all_stock_history_fields:
                # TODO: move all attributes to relevant cols
                # TODO: drop pointer
                pass
            elif c in all_market_history_fields:
                # TODO: move all attributes to relevant cols if in legal markets
                # TODO: drop pointer
                pass
        return df
