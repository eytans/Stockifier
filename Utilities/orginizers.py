import pymongo
import pickle
import os
import pandas as pd
import Utilities
import datetime
import enum
import gzip
from sklearn.preprocessing import StandardScaler, RobustScaler
from collections.abc import Mapping
import logging
import functools
import types

all_stocks_name = ['AFL', 'AIZ', 'CNO', 'EIG', 'GLRE', 'GTS', 'PRA', 'UNM', 'ACET', 'AI', 'APD', 'ARG', 'ASH', 'BAS',
                   'BCPC', 'CE', 'DOW', 'EMN', 'FF', 'FMC', 'HAL', 'HALO', 'HUN', 'LXU', 'MTX', 'PX', 'SHLM', 'TREC',
                   'TROX', 'AMAG', 'IDXX', 'NEOG', 'OXFD', 'QDEL', 'SRDX', 'VIVO', 'ALKS', 'BPTH', 'PETS', 'VRX',
                   'ABBV', 'AERI', 'AHS', 'ALIM', 'BMY', 'BXP', 'HRTX', 'IDT', 'IPXL', 'JNJ', 'KYTH', 'LLY', 'MRK',
                   'NANO', 'PFE', 'RMTI', 'RTRX', 'TXMD', 'ZGNX', 'AGN', 'DEPO', 'ENDP', 'ISIS', 'MEIP', 'OREX', 'POZN',
                   'PTX', 'SCLN', 'SCMP', 'SGYP', 'UTHR', 'PRGO', 'USNA', 'GNC', 'RAD', 'WBA', 'ABT', 'ADMS', 'AKRX',
                   'APH', 'BLT', 'CVT', 'FCSC', 'FLXN', 'GALT', 'HZNP', 'IRWD', 'KPTI', 'LCI', 'MDCO', 'MNK', 'MNTA',
                   'MYL', 'NATR', 'NBIX', 'NU', 'PCRX', 'RIGL', 'ROSE', 'SGNT', 'STAR', 'SUPN', 'TTPH', 'VSAR', 'ZTS',
                   'ABC', 'CAH', 'MCK', 'AET', 'ANTM', 'CI', 'CNC', 'CVS', 'ESRX', 'HIIQ', 'HUM', 'MGLN', 'MOH', 'UAM',
                   'UNH', 'WCG', 'ANH', 'BRC', 'CHH', 'CYH', 'HCA', 'LPNT', 'MED', 'NHC', 'SEM', 'THC', 'UHS', 'USMD',
                   'ACC', 'BKD', 'CSU', 'ENSG', 'FVE', 'KND', 'MET', 'REG', 'ABMD', 'ACRX', 'ADI', 'ALGN', 'AMT',
                   'ARAY', 'AXP', 'BABY', 'BIO', 'BSX', 'CNMD', 'COH', 'CRY', 'CSII', 'CUTR', 'CYBX', 'CYNO', 'ELX',
                   'EW', 'EXAC', 'GB', 'GME', 'GMED', 'GNMK', 'HOLX', 'IMI', 'ISRG', 'IVC', 'KTWO', 'LDRH', 'MASI',
                   'MDT', 'MDXG', 'NUVA', 'NXTM', 'OFIX', 'PHM', 'PHMD', 'RHT', 'RMD', 'RTIX', 'SIRO', 'SN', 'SPNC',
                   'STE', 'STJ', 'SUN', 'SYK', 'VAR', 'VASC', 'WMGI', 'ZBH', 'ZLTQ', 'ZMH', 'HSIC', 'OMI', 'PBH',
                   'PDCO', 'PGC', 'PMC', 'AKR', 'AMP', 'ANGO', 'ANN', 'ATEC', 'ATRC', 'ATRI', 'ATRS', 'BAX', 'BCR',
                   'BDX', 'BIOL', 'CMN', 'CMP', 'COO', 'DSCI', 'ELGX', 'HAE', 'HBIO', 'HRC', 'HTWR', 'IART', 'ICUI',
                   'IM', 'INGN', 'LMNX', 'MLAB', 'MMSI', 'MTD', 'OSUR', 'PM', 'PODD', 'SFL', 'STAA', 'TFX', 'THOR',
                   'TNDM', 'TRIV', 'TRNX', 'UNIS', 'UNS', 'UTMD', 'WAT', 'WST', 'XRAY', 'A', 'ABAX', 'AIQ', 'ALOG',
                   'ALR', 'AXDX', 'BEAT', 'BRKR', 'BRLI', 'COG', 'COV', 'CRL', 'DGX', 'DXCM', 'ENZ', 'EXAS', 'FLDM',
                   'FMI', 'GES', 'GHDX', 'LH', 'MBI', 'NEO', 'NSPH', 'PEB', 'PKI', 'PRXL', 'Q', 'RDNT', 'SSI', 'TEAR',
                   'TMO', 'ACHC', 'AMSG', 'DVA', 'HLS', 'HWAY', 'IPCM', 'MD', 'PAHC', 'PRSC', 'USPH', 'AAT', 'AGM',
                   'ALB', 'AMRS', 'CBT', 'CHMT', 'FOE', 'FUL', 'GPRE', 'GRA', 'HWKN', 'IFF', 'IOSP', 'IPHS', 'KMG',
                   'KOP', 'KRA', 'KRO', 'KWR', 'LYB', 'NEU', 'ODC', 'OLN', 'OMN', 'ORI', 'POL', 'PPG', 'RPM', 'SHW',
                   'SIAL', 'SNMX', 'SXT', 'SZYM', 'VAL', 'WDFC', 'WLK', 'AXLL']


# TODO: only supports one database for now!!! this needs to change for tests.
class DataAccessor(Mapping):
    class Names(enum.Enum):
        stock = 1
        quarter = 2
        for_clustering = 3

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
    # this dictionary contains a list of stock tickers for each market
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

    def __init_by_id_data(self, force=False):
        if self._market_by_id is None or force:
            self.__init_market_data(force=force)
            frames = self._market_data[self.database].values()
            self._market_by_id = pd.concat(frames)
            self._market_by_id = self._market_by_id.set_index('_id')

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

    @functools.lru_cache()
    def get_market_names(self):
        return self.markets.distinct('market_name')

    @functools.lru_cache()
    def get_stock_names(self):
        return self.stocks.distinct('ticker')

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


class TrainingData(object):
    def __init__(self, name, days_forward=1, startdate=None, enddate=None, threshold='default', ld=None):
        self.name = name
        self.ld = ld
        if ld is None:
            self.ld = LearningData()
        self.days_forward = days_forward
        self.data = self.ld.get_stock_data(name, startdate=startdate, enddate=enddate)
        if self.data.shape[0] + days_forward > self.ld.get_stock_data(name).shape[0]:
            self.data = self.data.iloc[0:self.ld.get_stock_data(name).shape[0] - (days_forward + self.data.shape[0])]
        self._threshold = None
        self.regulizer = StandardScaler()
        self._fitted = False
        self.set_threshold(threshold)

    def __repr__(self):
        return "TrainingData: name={}, days_forward={}".format(self.name, self.days_forward)

    def set_threshold(self, thresh):
        if thresh == 'default':
            thresh = 0
        elif thresh == 'middle':
            thresh = self.get_change().median()
        elif isinstance(thresh, float) and 1 > thresh > 0:
            thresh = self.get_change().quantile(thresh)
        else:
            if callable(thresh):
                self._threshold = thresh
                return self
            else:
                raise ValueError("Need to receive 'default' 'middle' number or function")
        self._threshold = lambda x: x > thresh
        logging.info("{}: threshold found is {}".format(self, thresh))
        return self

    def get_change(self):
        return self.ld.get_future_change_classification(self.data, self.name, self.days_forward)

    def add_history(self, stock_range, market_range=None, legal_markets=None):
        if not market_range:
            market_range = stock_range
        if not legal_markets:
            legal_markets = self.ld.get_market_names()

        full_data = self.ld.get_stock_data(self.name)

        if full_data.shape[0] < self.data.shape[0] + stock_range:
            self.data = self.data.iloc[self.data.shape[0] + stock_range - full_data.shape[0]:]
        for i in range(stock_range):
            if self.data.iloc[i].name == full_data.iloc[0].name:
                self.data = self.data.iloc[stock_range - i:]

        self.data.set_index([list(range(self.data.shape[0]))])

        for i in range(1, 1 + stock_range):
            end = self.data.iloc[-i]
            history_end_index = full_data.index.get_loc(end.name)
            history_start_index = history_end_index - self.data.shape[0]
            history_data = full_data.iloc[history_start_index:history_end_index]
            history_data.set_index([list(range(history_data.shape[0]))])

            for c in history_data.columns:
                self.data[Utilities.stock_history_field(i, c)] = history_data[c]

        for i in range(1, 1 + market_range):
            end = self.data.iloc[-i]
            for m in legal_markets:
                try:
                    history_data = self.ld.get_market_data(m).sort_index()
                    history_end_index = history_data.index.get_loc(end.name)
                    history_start_index = history_end_index - self.data.shape[0]
                    history_data = history_data.iloc[history_start_index:history_end_index]
                    history_data.set_index([list(range(history_data.shape[0]))])

                    for c in history_data.columns:
                        self.data[Utilities.market_history_field(i, m, c)] = history_data[c]
                except:
                    continue

        return self

    def drop_history(self, stock_history_range=None, market_history_range=None):
        all_market_history_fields, all_stock_history_fields = self._history_field_names()

        if stock_history_range:
            bad_stock_fields = set(all_stock_history_fields[stock_history_range:])
        else:
            bad_stock_fields = set(all_stock_history_fields)

        if market_history_range:
            bad_market_fields = set(all_market_history_fields[market_history_range * len(self.ld.get_market_names()):])
        else:
            bad_market_fields = set(all_market_history_fields)

        stock_drop_columns = [c for c in self.data.columns if c in bad_stock_fields]
        market_drop_columns = [c for c in self.data.columns if c in bad_market_fields]
        # drops all columns which shouldn't be here (all the names gathered)
        self.data.drop(stock_drop_columns + market_drop_columns, axis=1, inplace=True)
        return self

    def _history_field_names(self):
        # TODO: less hacky range
        stock_history_fields = [Utilities.stock_history_field(i) for i in range(0, 10000)]
        market_names = self.ld.get_market_names()
        market_history_fields = [Utilities.market_history_field(i, m) for i in range(0, 10000) for m in market_names]
        return market_history_fields, stock_history_fields

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

    def transform(self, data):
        if not self._fitted:
            self.data = self.regulizer.fit_transform(self.data)
            self._fitted = True
        return pd.DataFrame(self.regulizer.transform(data), index=data.index, columns=data.columns)

    @staticmethod
    def cleanup_data(data, fill=True):
        start_length = len(data)
        # drop rows with more then half of the values missing
        threshold = 0.5
        data = data.dropna(thresh=round(threshold*len(data.columns)))
        if start_length - len(data) > 0.1 * start_length:
            logging.warning(
                "dropped more then {} samples missing more then {}% of the values".format(start_length - len(data),
                                                                                         threshold*100))
        length = len(data)
        # drop columns with more then 20% of the values missing
        for col in data.columns:
            if data[col].isnull().sum() > 0.2 * length:
                logging.warning(
                    "dropping {} as it is missing {} values".format(col, data[col].isnull().sum()))
                data = data.drop(col, axis=1)
        # fill missing data with median
        if fill:
            data = data.fillna(data.mean())
        return data

    def get(self):
        if not self._fitted:
            # TODO: maybe drop change before transform
            self.data = self.cleanup_data(self.data)
            self.data = pd.DataFrame(self.regulizer.fit_transform(self.data), index=self.data.index,
                                     columns=self.data.columns)
            self._fitted = True
        return self.data, self.get_change().apply(self._threshold)
