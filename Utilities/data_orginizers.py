import pymongo
import pickle
import os
import pandas as pd
import Utilities
import datetime
import enum
import gzip
from pathos import multiprocessing
from collections.abc import Mapping


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


class LearningData(object):
    # TODO: only supports one database for now!!! this needs to change for tests.
    class DataAccessor(Mapping):
        class Names(enum.Enum):
            stock = 1

        def __init__(self, name):
            self.dir_path = os.path.join(Utilities.project_dir, 'cache')
            if not os.path.isdir(self.dir_path):
                os.makedirs(self.dir_path)
            if name not in LearningData.DataAccessor.Names:
                raise RuntimeError("bad name for data accessor")
            self.name = name

        def __get_file_name(self, item):
            return os.path.join(self.dir_path, '{}_{}.p.gz'.format(self.name, item))

        def __contains__(self, item):
            return os.path.exists(self.__get_file_name(item))

        def __getitem__(self, item):
            if not self.__contains__(item):
                raise KeyError(item)
            fn = self.__get_file_name(item)
            with gzip.open(fn, 'rb') as data:
                return pickle.load(data)

        def __setitem__(self, key, value):
            fn = self.__get_file_name(key)
            with gzip.open(fn, 'wb') as out:
                pickle.dump(value, out)

        def __iteration_helper(self):
            for f in os.listdir(self.dir_path):
                if f.startswith(self.name):
                    item = f.split('_')[1].split('.')[0]
                    yield item

        def __iter__(self):
            for item in self.__iteration_helper():
                yield item, self[item]

        def __len__(self):
            return len(list(self.__iteration_helper()))

    # save data as database to names to pandas.DataFrames
    _market_data = {}
    _stock_data = {}
    _stock_by_id = None
    _market_by_id = None

    def __init__(self, database='exchange', legal_markets=None):
        self.client = pymongo.MongoClient()
        db = self.client[database]
        self.database = database
        self.markets = db['markets']
        self.stocks = db['stocks']
        self.legal_markets = legal_markets
        if self.legal_markets is None:
            self.legal_markets = self.get_market_names()

    def __init_market_data(self, market_name=None, force=False):
        if self.database not in LearningData._market_data:
            LearningData._market_data[self.database] = {}
        data = LearningData._market_data[self.database]
        if market_name:
            if market_name not in data or force:
                query = {'market_name': market_name}
                data[market_name] = pd.DataFrame(list(self.markets.find(query))).set_index(['date'])
        else:
            for m in self.get_market_names():
                if m in data and not force:
                    continue
                query = {'market_name': m}
                data[m] = pd.DataFrame(list(self.markets.find(query))).set_index(['date'])

    def __init_stock_data(self, stock_name=None, force=False):
        if self.database not in LearningData._stock_data:
            self._stock_data[self.database] = self.DataAccessor(self.DataAccessor.Names.stock)
        data = self._stock_data[self.database]
        # TODO: non hacky version of date splitting preffered (so we wont timeout in mongo)
        middle = datetime.datetime(2005, 1, 1)
        if stock_name:
            if stock_name not in data or force:
                name = stock_name
                ld = LearningData()
                query = {'ticker': name}
                query['date'] = {'$lt': middle}
                first = pd.DataFrame(list(ld.stocks.find(query)))
                query['date'] = {'$gte': middle}
                second = pd.DataFrame(list(ld.stocks.find(query)))
                data[name] = pd.concat([first, second]).set_index(['date'])
        else:
            names = filter(lambda name: name not in data or force, list(self.stocks.distinct('ticker')))
            for name in names:
                self.__init_stock_data(name, force)

            # def work_on_it(name):
            #     ld = LearningData()
            #     query = {'ticker': name}
            #     query['date'] = {'$lt': middle}
            #     first = pd.DataFrame(list(ld.stocks.find(query)))
            #     query['date'] = {'$gte': middle}
            #     second = pd.DataFrame(list(ld.stocks.find(query)))
            #     data[name] = pd.concat([first, second]).set_index(['date'])
            #
            # p.map(work_on_it, names)

    def __init_by_id_data(self, force=False):
        if self._market_by_id is None or force:
            self.__init_market_data(force=force)
            frames = self._market_data[self.database].values()
            self._market_by_id = pd.concat(frames)
            self._market_by_id = self._market_by_id.set_index('_id')
            self._market_by_id = self.drop_history_fields(self._market_by_id)
        if self._stock_by_id is None or force:
            self.__init_stock_data(force=force)
            frames = None
            for key, df in self._stock_data[self.database]:
                cleaned = self.drop_history_fields(df)
                if not frames:
                    frames = cleaned
                else:
                    frames = pd.concat([cleaned, frames])
            self._stock_by_id = frames.set_index('_id')

    def get_future_change_classification(self, data, stock_name, days_forward):
        full_data = self.get_stock_data(stock_name)
        start = data.iloc[days_forward]
        data_start_index = full_data.index.get_loc(start.name)
        data_end_index = data_start_index + data.shape[0]
        result_data = full_data.iloc[data_start_index:data_end_index]['change']
        return result_data

    @classmethod
    def save(cls, path=None):
        if not path:
            path = Utilities.default_pickle
        data = (cls._market_data, cls._market_by_id, cls._stock_by_id)
        with gzip.open(path, 'wb') as out:
            pickle.dump(data, out)

    @classmethod
    def load(cls, path=None):
        if not os.path.exists(path):
            return
        with gzip.open(path, 'rb') as data:
            cls._market_data, cls._market_by_id, cls._stock_by_id = pickle.load(data)

    def get_market_data(self, market_name=None, startdate=None, enddate=None, force=False):
        self.__init_market_data(market_name, force)
        if not market_name:
            return LearningData._market_data[self.database]
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

    def get_stock_data(self, stock_name, startdate=None, enddate=None, force=False):
        self.__init_stock_data(stock_name, force)
        if not stock_name:
            return LearningData._stock_data[self.database]
        else:
            return self.slice_by_date(LearningData._stock_data[self.database][stock_name], startdate, enddate)

    def flat_pointers(self, df, stock_range, market_range=None, legal_markets=None):
        if not market_range:
            market_range = stock_range
        market_history_fields, stock_history_fields = self._history_field_names()
        self.drop_history_fields(df, stock_range, market_range)
        # now for all fields that weren't dropped start creating a ton of features

        self.__init_by_id_data()

        # TODO: add columns for flattened attributes
        stock_columns = [c for c in df.columns if c in stock_history_fields]
        joined = df.join([self._stock_by_id]*len(stock_columns), on=stock_columns)

        market_columns = [c for c in df.columns if c in market_history_fields]
        joined = joined.join([self._market_by_id] * len(market_columns), on=market_columns)


        # # TODO: iter rows to fill data
        # for c in df.columns:
        #     if c in stock_history_fields:
        #         # TODO: move all attributes to relevant cols
        #
        #         pass
        #     elif c in market_history_fields:
        #         # TODO: move all attributes to relevant cols if in legal markets
        #         pass
        #
        # # TODO: drop all pointers when done with object ids
        return joined

    def drop_history_fields(self, df, stock_history_range=None, market_history_range=None):
        all_market_history_fields, all_stock_history_fields = self._history_field_names()

        if stock_history_range:
            bad_stock_fields = set(all_stock_history_fields[stock_history_range:])
        else:
            bad_stock_fields = set(all_stock_history_fields)

        if market_history_range:
            bad_market_fields = set(all_market_history_fields[market_history_range*len(self.get_market_names()):])
        else:
            bad_market_fields = set(all_market_history_fields)

        stock_drop_columns = [c for c in df.columns if c in bad_stock_fields]
        market_drop_columns = [c for c in df.columns if c in bad_market_fields]
        # drops all columns which shouldn't be here (all the names gathered)
        return df.drop(stock_drop_columns + market_drop_columns, axis=1)

    def get_market_names(self):
        return self.markets.distinct('market_name')

    def get_stock_names(self):
        return self.stocks.distinct('ticker')

    def _history_field_names(self):
        # TODO: less hacky range
        stock_history_fields = [Utilities.stock_history_field(i) for i in range(0, 10000)]
        market_names = self.get_market_names()
        market_history_fields = [Utilities.market_history_field(i, m) for i in range(0, 10000) for m in market_names]
        return market_history_fields, stock_history_fields


