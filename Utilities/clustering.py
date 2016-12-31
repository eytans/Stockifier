import sklearn.cluster
from Utilities.orginizers import LearningData,DataAccessor
import pandas as pd
import numpy as np

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

example_stocks = ['AFL', 'AIZ', 'CNO', 'EIG', 'GLRE', 'GTS', 'PRA', 'UNM']

market_stock_dic = {
    'Drug Manufacturers - Major (Healthcare)': ['ABBV', 'AERI', 'ALIM', 'BMY', 'BXP', 'HRTX', 'IDT', 'IPXL', 'JNJ',
                                                'KYTH', 'LLY', 'NANO', 'PFE', 'RMTI', 'RTRX', 'TXMD', 'ZGNX'],
    'Medical Equipment Wholesale (Services)': ['CAH', 'HSIC', 'OMI', 'PBH', 'PDCO', 'PGC', 'PMC'],
    'Diagnostic Substances (Healthcare)': ['AMAG', 'IDXX', 'NEOG', 'OXFD', 'QDEL', 'SRDX', 'VIVO'],
    'Drug Stores (Services)': ['GNC', 'RAD', 'WBA'],
    'Hospitals (Healthcare)': ['ANH', 'BRC', 'CHH', 'CYH', 'HCA', 'LPNT', 'SEM', 'THC', 'UHS', 'USMD'],
    'Specialty Chemicals (Basic Materials)': ['CNO', 'GTS', 'AAT', 'AGM', 'ALB', 'AMRS', 'CBT', 'CHMT', 'FOE', 'FUL',
                                              'GPRE', 'GRA', 'HWKN', 'IFF', 'IOSP', 'IPHS', 'KMG', 'KOP', 'KRA', 'KRO',
                                              'KWR', 'LYB', 'NEU', 'ODC', 'OLN', 'OMN', 'ORI', 'POL', 'PPG', 'RPM',
                                              'SHW', 'SIAL', 'SNMX', 'SXT', 'SZYM', 'VAL', 'WDFC', 'WLK'],
    'Drug Delivery (Healthcare)': ['ALKS', 'BPTH', 'PETS'],
    'Chemicals - Major Diversified (Basic Materials)': ['ACET', 'AI', 'APD', 'ARG', 'ASH', 'BAS', 'BCPC', 'CE', 'DOW',
                                                        'EMN', 'FF', 'FMC', 'HAL', 'HALO', 'HUN', 'LXU', 'MTX', 'PX',
                                                        'SHLM', 'TREC', 'TROX'],
    'Drug Manufacturers - Other (Healthcare)': ['AGN', 'DEPO', 'ENDP', 'ISIS', 'MEIP', 'OREX', 'POZN', 'PTX', 'SCLN',
                                                'SCMP', 'SGYP', 'UTHR'],
    'Accident & Health Insurance (Financial)': ['AFL', 'AIZ', 'EIG', 'GLRE', 'PRA', 'UNM'],
    'Drugs - Generic (Healthcare)': ['VRX', 'MRK', 'ADMS', 'AKRX', 'APH', 'BLT', 'CVT', 'FCSC', 'FLXN', 'GALT', 'HZNP',
                                     'IRWD', 'KPTI', 'LCI', 'MDCO', 'MNK', 'MNTA', 'MYL', 'NATR', 'NBIX', 'NU', 'PCRX',
                                     'RIGL', 'ROSE', 'SGNT', 'STAR', 'SUPN', 'TTPH', 'VSAR', 'ZTS'],
    'Specialized Health Services (Healthcare)': ['AHS', 'ACHC', 'AMSG', 'DVA', 'HLS', 'HWAY', 'IPCM', 'MD', 'PAHC',
                                                 'PRSC', 'USPH'],
    'Health Care Plans (Healthcare)': ['AET', 'ANTM', 'CI', 'CNC', 'CVS', 'ESRX', 'HIIQ', 'HUM', 'MGLN', 'MOH', 'UAM',
                                       'UNH', 'WCG'],
    'Medical Laboratories & Research (Healthcare)': ['BIO', 'A', 'ABAX', 'AIQ', 'ALOG', 'ALR', 'AXDX', 'BEAT', 'BRKR',
                                                     'BRLI', 'COG', 'COV', 'CRL', 'DGX', 'DXCM', 'ENZ', 'EXAS', 'FLDM',
                                                     'FMI', 'GES', 'GHDX', 'LH', 'MBI', 'NEO', 'NSPH', 'PEB', 'PKI',
                                                     'PRXL', 'Q', 'RDNT', 'SSI', 'TEAR', 'TMO'],
    'Long-Term Care Facilities (Healthcare)': ['NHC', 'ACC', 'BKD', 'CSU', 'ENSG', 'FVE', 'KND', 'MET', 'REG'],
    'Drugs Wholesale (Services)': ['ABC', 'MCK'], 'Synthetics (Basic Materials)': ['AXLL'],
    'Medical Appliances & Equipment (Healthcare)': ['ABT', 'MED', 'ABMD', 'ACRX', 'ADI', 'ALGN', 'AMT', 'ARAY', 'AXP',
                                                    'BABY', 'BSX', 'CNMD', 'COH', 'CRY', 'CSII', 'CUTR', 'CYBX', 'CYNO',
                                                    'ELX', 'EW', 'EXAC', 'GB', 'GME', 'GMED', 'GNMK', 'HOLX', 'IMI',
                                                    'ISRG', 'IVC', 'KTWO', 'LDRH', 'MASI', 'MDT', 'MDXG', 'NUVA',
                                                    'NXTM', 'OFIX', 'PHM', 'PHMD', 'RHT', 'RTIX', 'SIRO', 'SN', 'SPNC',
                                                    'STE', 'STJ', 'SUN', 'SYK', 'VAR', 'VASC', 'WMGI', 'ZBH', 'ZLTQ',
                                                    'ZMH'], 'Drug Related Products (Healthcare)': ['PRGO', 'USNA'],
    'Medical Instruments & Supplies (Healthcare)': ['RMD', 'AKR', 'AMP', 'ANGO', 'ANN', 'ATEC', 'ATRC', 'ATRI', 'ATRS',
                                                    'BAX', 'BCR', 'BDX', 'BIOL', 'CMN', 'CMP', 'COO', 'DSCI', 'ELGX',
                                                    'HAE', 'HBIO', 'HRC', 'HTWR', 'IART', 'ICUI', 'IM', 'INGN', 'LMNX',
                                                    'MLAB', 'MMSI', 'MTD', 'OSUR', 'PM', 'PODD', 'SFL', 'STAA', 'TFX',
                                                    'THOR', 'TNDM', 'TRIV', 'TRNX', 'UNIS', 'UNS', 'UTMD', 'WAT', 'WST',
                                                    'XRAY']}


class StrengthCalc(object):
    def __init__(self, start_date="1995-01-01", stock_list=None, freq="BQ", periods=(2016 - 1995) * 4 + 3):
        self._accessor = DataAccessor(DataAccessor.Names.for_clustering)
        self._ready = False
        self.data = {}
        self.data_to_fit =[]
        self.start = start_date
        self.ld = LearningData()
        self.stocks = stock_list
        if self.stocks is None:
            self.stocks = self.ld.get_stock_names()
        self.freq = freq
        self.periods = periods
        self.__init_data()

    def __combined_stock_name(self, st):
        return st + str(self.start) + str(self.freq) + str(self.periods)

    def __init_data(self):
        date_array = pd.bdate_range(start=self.start, periods=self.periods, freq=self.freq)
        for st in self.stocks:
            if self.__combined_stock_name(st) not in self._accessor:
                current_stock_data = self.ld.get_stock_data(st)
                # need to take in consideration case of "inf" in value
                # gets the open and volume of the current df and calculate the percentage of change
                try:
                    value = current_stock_data.loc[date_array][['open', 'volume']]
                except:
                    print(st)
                    continue
                # fill NaN with mean of the column
                value = value.reset_index()
                value.columns = ['time', 'open', 'volume']
                value = value.drop_duplicates('time').set_index('time')
                value = value.fillna(value.mean())
                # volume at the before exist is 0
                value = value.replace('inf', 0.0)
                # need to take the two columns and create a feature row from it. (single row for cluster)
                # we have 2 columns, open and volume and many dates.
                self._accessor[self.__combined_stock_name(st)] = value
            self.data[st] = self._accessor[self.__combined_stock_name(st)]
            self.data_to_fit.append(self.data[st].values)
        self.data_to_fit = np.vstack(np.dstack(self.data_to_fit)).T

    def ready_stock_to_predict(self, stocks):
        data_arr = []
        for st in stocks:
            data_arr.append(self.data[st].values)
        return np.vstack(np.dstack(data_arr)).T

    def create_clustering_obj(self, n_clusters):
        clr = sklearn.cluster.KMeans(n_clusters=n_clusters)
        clr.fit(self.data_to_fit, self.stocks)
        return clr

    def create_array_of_clusters(self, min_number=3, max_number=120, step=None):
        arr_clr = []
        for x in range(min_number, max_number + 1, step):
            arr_clr.append(self.create_clustering_obj(n_clusters=x))
        return arr_clr

    def get_strength(self, stock, market, min_number, max_number, step, threshold=0.75):
        market = market_stock_dic[market]
        arr_clr = self.create_array_of_clusters(min_number=min_number,max_number=max_number, step=step)
        arr_clr.reverse()
        stock_data = self.ready_stock_to_predict([stock])
        market_data = self.ready_stock_to_predict(market)
        strength = 1.0
        for a in arr_clr:
            count = 0
            stock_label = a.predict(stock_data)
            market_labels = a.predict(market_data)
            for m in market_labels:
                if stock_label == m:
                    count += 1
            if count / len(market_labels) > threshold:
                return strength
            else:
                strength -= 1 / len(arr_clr)
                strength = round(strength,2)
        return strength
# print(get_strength(stock='NHC',market='Medical Laboratories & Research (Healthcare)',min_number=5,max_number=20,step=5))