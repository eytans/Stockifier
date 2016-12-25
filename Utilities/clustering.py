import sklearn.cluster
from Utilities.orginizers import LearningData
import pandas as pd
import itertools
import numpy as np


all_stocks_name = ['AFL', 'AIZ', 'CNO', 'EIG', 'GLRE', 'GTS', 'PRA', 'UNM', 'ACET', 'AI', 'APD', 'ARG', 'ASH', 'BAS', 'BCPC', 'CE', 'DOW', 'EMN', 'FF', 'FMC', 'HAL', 'HALO', 'HUN', 'LXU', 'MTX', 'PX', 'SHLM', 'TREC', 'TROX', 'AMAG', 'IDXX', 'NEOG', 'OXFD', 'QDEL', 'SRDX', 'VIVO', 'ALKS', 'BPTH', 'PETS', 'VRX', 'ABBV', 'AERI', 'AHS', 'ALIM', 'BMY', 'BXP', 'HRTX', 'IDT', 'IPXL', 'JNJ', 'KYTH', 'LLY', 'MRK', 'NANO', 'PFE', 'RMTI', 'RTRX', 'TXMD', 'ZGNX', 'AGN', 'DEPO', 'ENDP', 'ISIS', 'MEIP', 'OREX', 'POZN', 'PTX', 'SCLN', 'SCMP', 'SGYP', 'UTHR', 'PRGO', 'USNA', 'GNC', 'RAD', 'WBA', 'ABT', 'ADMS', 'AKRX', 'APH', 'BLT', 'CVT', 'FCSC', 'FLXN', 'GALT', 'HZNP', 'IRWD', 'KPTI', 'LCI', 'MDCO', 'MNK', 'MNTA', 'MYL', 'NATR', 'NBIX', 'NU', 'PCRX', 'RIGL', 'ROSE', 'SGNT', 'STAR', 'SUPN', 'TTPH', 'VSAR', 'ZTS', 'ABC', 'CAH', 'MCK', 'AET', 'ANTM', 'CI', 'CNC', 'CVS', 'ESRX', 'HIIQ', 'HUM', 'MGLN', 'MOH', 'UAM', 'UNH', 'WCG', 'ANH', 'BRC', 'CHH', 'CYH', 'HCA', 'LPNT', 'MED', 'NHC', 'SEM', 'THC', 'UHS', 'USMD', 'ACC', 'BKD', 'CSU', 'ENSG', 'FVE', 'KND', 'MET', 'REG', 'ABMD', 'ACRX', 'ADI', 'ALGN', 'AMT', 'ARAY', 'AXP', 'BABY', 'BIO', 'BSX', 'CNMD', 'COH', 'CRY', 'CSII', 'CUTR', 'CYBX', 'CYNO', 'ELX', 'EW', 'EXAC', 'GB', 'GME', 'GMED', 'GNMK', 'HOLX', 'IMI', 'ISRG', 'IVC', 'KTWO', 'LDRH', 'MASI', 'MDT', 'MDXG', 'NUVA', 'NXTM', 'OFIX', 'PHM', 'PHMD', 'RHT', 'RMD', 'RTIX', 'SIRO', 'SN', 'SPNC', 'STE', 'STJ', 'SUN', 'SYK', 'VAR', 'VASC', 'WMGI', 'ZBH', 'ZLTQ', 'ZMH', 'HSIC', 'OMI', 'PBH', 'PDCO', 'PGC', 'PMC', 'AKR', 'AMP', 'ANGO', 'ANN', 'ATEC', 'ATRC', 'ATRI', 'ATRS', 'BAX', 'BCR', 'BDX', 'BIOL', 'CMN', 'CMP', 'COO', 'DSCI', 'ELGX', 'HAE', 'HBIO', 'HRC', 'HTWR', 'IART', 'ICUI', 'IM', 'INGN', 'LMNX', 'MLAB', 'MMSI', 'MTD', 'OSUR', 'PM', 'PODD', 'SFL', 'STAA', 'TFX', 'THOR', 'TNDM', 'TRIV', 'TRNX', 'UNIS', 'UNS', 'UTMD', 'WAT', 'WST', 'XRAY', 'A', 'ABAX', 'AIQ', 'ALOG', 'ALR', 'AXDX', 'BEAT', 'BRKR', 'BRLI', 'COG', 'COV', 'CRL', 'DGX', 'DXCM', 'ENZ', 'EXAS', 'FLDM', 'FMI', 'GES', 'GHDX', 'LH', 'MBI', 'NEO', 'NSPH', 'PEB', 'PKI', 'PRXL', 'Q', 'RDNT', 'SSI', 'TEAR', 'TMO', 'ACHC', 'AMSG', 'DVA', 'HLS', 'HWAY', 'IPCM', 'MD', 'PAHC', 'PRSC', 'USPH', 'AAT', 'AGM', 'ALB', 'AMRS', 'CBT', 'CHMT', 'FOE', 'FUL', 'GPRE', 'GRA', 'HWKN', 'IFF', 'IOSP', 'IPHS', 'KMG', 'KOP', 'KRA', 'KRO', 'KWR', 'LYB', 'NEU', 'ODC', 'OLN', 'OMN', 'ORI', 'POL', 'PPG', 'RPM', 'SHW', 'SIAL', 'SNMX', 'SXT', 'SZYM', 'VAL', 'WDFC', 'WLK', 'AXLL']

example_stocks = ['AFL', 'AIZ', 'CNO', 'EIG', 'GLRE', 'GTS', 'PRA', 'UNM']
# def find_maximal_for_stock_and_market(self, path_to_stock,path_to_market):
#     first,last = self.maximal_shared_range_dir(path_to_market)
#     stock_file = open(path_to_stock,'r')
#     list_of_all_dates = []
#     for line in stock_file.readlines():
#         list_of_all_dates.append(line.split(',')[1])
#     if first < self.getdate(list_of_all_dates[0]):
#         first = self.getdate(list_of_all_dates[0])
#     if last > self.getdate(list_of_all_dates[len(list_of_all_dates)-1]):
#         last = self.getdate(list_of_all_dates[len(list_of_all_dates)-1])
#     return first, last


def find_smallest_common(self,s1,s2):
    """
    This function excepts two stocks and returns how up you need to go in the tree in order for the stocks to
    be at the same cluster
    :return:
    """


def get_data(start_date="1995-01-01", stock_list=None , freq="BQ", periods=(2016-1995)*4+3):
    """
    :param start_date:
    :param stock_list:
    :param freq:
    :param periods:
    :return:
    """
    ld = LearningData()
    if not stock_list:
        stock_list = all_stocks_name
    date_array = pd.bdate_range(start=start_date, periods=periods, freq=freq)
    data = []
    for st in stock_list:
        current_stock_data = ld.get_stock_data(st)
        # need to take in consideration case of "inf" in value
        # gets the open and volume of the current df and calculate the percentage of change
        value = current_stock_data.loc[date_array][['open', 'volume']]
        # fill NaN with mean of the column
        value = value.reset_index()
        value.columns = ['time', 'open', 'volume']
        value = value.drop_duplicates('time').set_index('time')
        value = value.fillna(value.mean())
        # volume at the before exist is 0
        value = value.replace('inf', 0.0)
        # need to take the two columns and create a feature row from it. (single row for cluster)
        # we have 2 columns, open and volume and many dates.
        data.append(value.values)
    return np.vstack(np.dstack(data)).T

def create_clustering_obj(n_clusters,data,stock_list):
    clr = sklearn.cluster.KMeans(n_clusters=n_clusters)
    clr.fit(data, stock_list)
    return clr

def create_array_of_clusters(stock_list,start_date=None ,min_number=3,max_number=120):
    data = get_data(start_date=start_date, stock_list=stock_list)
    arr_clr = []
    for x in range(min_number,max_number+1):
        arr_clr.append(create_clustering_obj(n_clusters=x,data=data,stock_list=stock_list))

# def get_relation(stock,market,start_date=None ,stock_list=None):


