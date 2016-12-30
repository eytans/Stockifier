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

all_stocks_name = ['AFL', 'AIZ', 'CNO', 'EIG', 'GLRE', 'GTS', 'PRA', 'UNM', 'ACET', 'AI', 'APD', 'ARG', 'ASH', 'BAS', 'BCPC', 'CE', 'DOW', 'EMN', 'FF', 'FMC', 'HAL', 'HALO', 'HUN', 'LXU', 'MTX', 'PX', 'SHLM', 'TREC', 'TROX', 'AMAG', 'IDXX', 'NEOG', 'OXFD', 'QDEL', 'SRDX', 'VIVO', 'ALKS', 'BPTH', 'PETS', 'VRX', 'ABBV', 'AERI', 'AHS', 'ALIM', 'BMY', 'BXP', 'HRTX', 'IDT', 'IPXL', 'JNJ', 'KYTH', 'LLY', 'MRK', 'NANO', 'PFE', 'RMTI', 'RTRX', 'TXMD', 'ZGNX', 'AGN', 'DEPO', 'ENDP', 'ISIS', 'MEIP', 'OREX', 'POZN', 'PTX', 'SCLN', 'SCMP', 'SGYP', 'UTHR', 'PRGO', 'USNA', 'GNC', 'RAD', 'WBA', 'ABT', 'ADMS', 'AKRX', 'APH', 'BLT', 'CVT', 'FCSC', 'FLXN', 'GALT', 'HZNP', 'IRWD', 'KPTI', 'LCI', 'MDCO', 'MNK', 'MNTA', 'MYL', 'NATR', 'NBIX', 'NU', 'PCRX', 'RIGL', 'ROSE', 'SGNT', 'STAR', 'SUPN', 'TTPH', 'VSAR', 'ZTS', 'ABC', 'CAH', 'MCK', 'AET', 'ANTM', 'CI', 'CNC', 'CVS', 'ESRX', 'HIIQ', 'HUM', 'MGLN', 'MOH', 'UAM', 'UNH', 'WCG', 'ANH', 'BRC', 'CHH', 'CYH', 'HCA', 'LPNT', 'MED', 'NHC', 'SEM', 'THC', 'UHS', 'USMD', 'ACC', 'BKD', 'CSU', 'ENSG', 'FVE', 'KND', 'MET', 'REG', 'ABMD', 'ACRX', 'ADI', 'ALGN', 'AMT', 'ARAY', 'AXP', 'BABY', 'BIO', 'BSX', 'CNMD', 'COH', 'CRY', 'CSII', 'CUTR', 'CYBX', 'CYNO', 'ELX', 'EW', 'EXAC', 'GB', 'GME', 'GMED', 'GNMK', 'HOLX', 'IMI', 'ISRG', 'IVC', 'KTWO', 'LDRH', 'MASI', 'MDT', 'MDXG', 'NUVA', 'NXTM', 'OFIX', 'PHM', 'PHMD', 'RHT', 'RMD', 'RTIX', 'SIRO', 'SN', 'SPNC', 'STE', 'STJ', 'SUN', 'SYK', 'VAR', 'VASC', 'WMGI', 'ZBH', 'ZLTQ', 'ZMH', 'HSIC', 'OMI', 'PBH', 'PDCO', 'PGC', 'PMC', 'AKR', 'AMP', 'ANGO', 'ANN', 'ATEC', 'ATRC', 'ATRI', 'ATRS', 'BAX', 'BCR', 'BDX', 'BIOL', 'CMN', 'CMP', 'COO', 'DSCI', 'ELGX', 'HAE', 'HBIO', 'HRC', 'HTWR', 'IART', 'ICUI', 'IM', 'INGN', 'LMNX', 'MLAB', 'MMSI', 'MTD', 'OSUR', 'PM', 'PODD', 'SFL', 'STAA', 'TFX', 'THOR', 'TNDM', 'TRIV', 'TRNX', 'UNIS', 'UNS', 'UTMD', 'WAT', 'WST', 'XRAY', 'A', 'ABAX', 'AIQ', 'ALOG', 'ALR', 'AXDX', 'BEAT', 'BRKR', 'BRLI', 'COG', 'COV', 'CRL', 'DGX', 'DXCM', 'ENZ', 'EXAS', 'FLDM', 'FMI', 'GES', 'GHDX', 'LH', 'MBI', 'NEO', 'NSPH', 'PEB', 'PKI', 'PRXL', 'Q', 'RDNT', 'SSI', 'TEAR', 'TMO', 'ACHC', 'AMSG', 'DVA', 'HLS', 'HWAY', 'IPCM', 'MD', 'PAHC', 'PRSC', 'USPH', 'AAT', 'AGM', 'ALB', 'AMRS', 'CBT', 'CHMT', 'FOE', 'FUL', 'GPRE', 'GRA', 'HWKN', 'IFF', 'IOSP', 'IPHS', 'KMG', 'KOP', 'KRA', 'KRO', 'KWR', 'LYB', 'NEU', 'ODC', 'OLN', 'OMN', 'ORI', 'POL', 'PPG', 'RPM', 'SHW', 'SIAL', 'SNMX', 'SXT', 'SZYM', 'VAL', 'WDFC', 'WLK', 'AXLL']

# TODO: only supports one database for now!!! this needs to change for tests.
class DataAccessor(Mapping):
    class Names(enum.Enum):
        stock = 1
        quarter = 2

    def __init__(self, name):
        self.dir_path = os.path.join(Utilities.project_dir, 'cache')
        if not os.path.isdir(self.dir_path):
            os.makedirs(self.dir_path)
        if name not in DataAccessor.Names:
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


class LearningData(object):
    # save data as database to names to pandas.DataFrames
    _market_data = {}
    _stock_data = {}
    _market_by_id = None
    #this dictionary contains a list of stock tickers for each market
    _market_dic = dict()

    def __init__(self, database='exchange', legal_markets=None,
                 cols_to_drop=('_id', 'adj_low', 'adj_close', 'adj_open', 'adj_volume', 'adj_high', 'market_name',
                               'ticker'),
                 market_cols_drop=('market_name', '_id')):
        self.client = pymongo.MongoClient()
        db = self.client[database]
        self.database = database
        self.markets = db['markets']
        self.stocks = db['stocks']
        self.legal_markets = legal_markets
        self.cols_to_drop = list(cols_to_drop)
        self.cols_to_drop_markets = list(market_cols_drop)
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
            self._stock_data[self.database] = DataAccessor(DataAccessor.Names.stock)
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
        if data_end_index > full_data.shape[0]:
            raise RuntimeError("cant get forward classification as not data forward")
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
            return {key: val.drop(self.cols_to_drop_markets, axis=1) for key, val in
                    LearningData._market_data[self.database].items}
        else:
            df = LearningData._market_data[self.database][market_name].drop(self.cols_to_drop_markets, axis=1)
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
        temp = self.slice_by_date(self._stock_data[self.database][stock_name], startdate, enddate)
        return temp.drop(list(self.cols_to_drop), axis=1)

    def add_history_fields(self, data, stock_name, stock_range, market_range=None, legal_markets=None):
        if not market_range:
            market_range = stock_range
        if not legal_markets:
            if self.legal_markets:
                legal_markets = self.legal_markets
            else:
                legal_markets = self.get_market_names()

        res_data = data.copy(False)
        full_data = self.get_stock_data(stock_name)

        if full_data.shape[0] < res_data.shape[0] + stock_range:
            res_data = res_data.iloc[res_data.shape[0] + stock_range - full_data.shape[0]:]
        for i in range(stock_range):
            if res_data.iloc[i].name == full_data.iloc[0].name:
                res_data = res_data.iloc[stock_range - i:]

        res_data.set_index([list(range(res_data.shape[0]))])

        for i in range(1, 1 + stock_range):
            end = res_data.iloc[-i]
            history_end_index = full_data.index.get_loc(end.name)
            history_start_index = history_end_index - res_data.shape[0]
            history_data = full_data.iloc[history_start_index:history_end_index]
            history_data.set_index([list(range(history_data.shape[0]))])

            for c in history_data.columns:
                res_data[Utilities.stock_history_field(i, c)] = history_data[c]

        for i in range(1, 1 + market_range):
            end = data.iloc[-i]
            for m in legal_markets:
                try:
                    history_data = self.get_market_data(m)
                    history_end_index = history_data.index.get_loc(end.name)
                    history_start_index = history_end_index - data.shape[0]
                    history_data = history_data.iloc[history_start_index:history_end_index]
                    history_data.set_index([list(range(history_data.shape[0]))])

                    for c in history_data.columns:
                        res_data[Utilities.market_history_field(i, m, c)] = history_data[c]
                except:
                    continue

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

    def get_market_stock_dic(self):
        """
        :return: a dictionary that contains for each market a list of stocks.
        """
        all_stocks = all_stocks_name
        all_markets = self.get_market_names()
        market_dic = dict.fromkeys(all_markets)
        for st in all_stocks:
            query = {'ticker': st}
            current_data = pd.DataFrame(list(self.stocks.find(query).limit(2)))
            market = current_data.market_name.tolist()[0]
            if market_dic[market] is None:
                market_dic[market] = [st]
            else:
                market_dic[market] += [st]
        return market_dic


