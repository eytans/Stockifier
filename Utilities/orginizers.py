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
            self.name = str(name)

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
                # drop duplicates
                with_dups = pd.concat([first, second]).set_index(['date'])
                without_dups = with_dups[~with_dups.index.duplicated()]
                # also drop fields where open is not a number (god knows why we have such entries)
                without_empty_open = without_dups[without_dups.apply(lambda row: not isinstance(row['open'], str),
                                                                     axis=1)]
                data[name] = without_empty_open
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
        data = (cls._market_data, cls._market_by_id)
        with gzip.open(path, 'wb') as out:
            pickle.dump(data, out)

    @classmethod
    def load(cls, path=None):
        if not os.path.exists(path):
            return
        with gzip.open(path, 'rb') as data:
            cls._market_data, cls._market_by_id = pickle.load(data)

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

    def get_stock_data(self, stock_name=None, startdate=None, enddate=None, force=False):
        self.__init_stock_data(stock_name, force)
        if not stock_name:
            return LearningData._stock_data[self.database]
        else:
            return self.slice_by_date(LearningData._stock_data[self.database][stock_name], startdate, enddate)

    def add_history_fields(self, data, stock_name, stock_range, market_range=None, legal_markets=None):
        if not market_range:
            market_range = stock_range
        if not legal_markets:
            legal_markets = self.get_market_names()

        res_data = data.copy(False)
        full_data = self.get_stock_data(stock_name)

        if full_data.shape[0] < res_data.shape[0] + stock_range:
            res_data = res_data.iloc[res_data.shape[0] + stock_range - full_data.shape[0]:]

        for i in range(1, 1 + stock_range):
            end = data.iloc[-i]
            history_end_index = full_data.index.get_loc(end.name)
            history_start_index = history_end_index - data.shape[0]
            history_data = full_data.iloc[history_start_index:history_end_index]

            for c in history_data.columns:
                res_data[Utilities.stock_history_field(i, c)] = history_data[c]

        for i in range(1, 1 + market_range):
            end = data.iloc[-i]
            for m in legal_markets:
                history_data = self.get_market_data(m)
                history_end_index = history_data.index.get_loc(end.name)
                history_start_index = history_end_index - data.shape[0]
                history_data = history_data.iloc[history_start_index:history_end_index]

                for c in history_data.columns:
                    res_data[Utilities.market_history_field(i, m, c)] = history_data[c]

        return res_data

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
