import re
import os


project_dir = os.path.dirname(os.path.dirname(__file__))
utilities_dir = os.path.dirname(__file__)
default_pickle = os.path.join(project_dir, 'learning_data.pickle')

_cleaning_regex = re.compile('[^a-zA-Z_]')


def stock_history_field(day, field=''):
    return field+str(day)+'_days_before'


def clean_market_name(market):
    return _cleaning_regex.sub('', market.replace(" ", "_"))


def market_history_field(day, market, field=''):
    return field + clean_market_name(market) + '_' + str(day) + '_days_before'


def dataframe_safe_loc(df, row_name):
    try:
        return df.loc[row_name]
    except:
        return None


def dataframe_safe_get_value(df, row_name, col):
    try:
        return df.get_value(row_name, col)
    except:
        return None


def iterate_couples(it):
    prev = None
    first = True
    for i in it:
        if first:
            prev = i
            first = False
            continue
        yield prev, i
        prev = i

all_stocks_name = ['AFL', 'AIZ', 'CNO', 'EIG', 'GLRE', 'GTS', 'PRA', 'UNM', 'ACET', 'AI', 'APD', 'ARG', 'ASH', 'BAS', 'BCPC', 'CE', 'DOW', 'EMN', 'FF', 'FMC', 'HAL', 'HALO', 'HUN', 'LXU', 'MTX', 'PX', 'SHLM', 'TREC', 'TROX', 'AMAG', 'IDXX', 'NEOG', 'OXFD', 'QDEL', 'SRDX', 'VIVO', 'ALKS', 'BPTH', 'PETS', 'VRX', 'ABBV', 'AERI', 'AHS', 'ALIM', 'BMY', 'BXP', 'HRTX', 'IDT', 'IPXL', 'JNJ', 'KYTH', 'LLY', 'MRK', 'NANO', 'PFE', 'RMTI', 'RTRX', 'TXMD', 'ZGNX', 'AGN', 'DEPO', 'ENDP', 'ISIS', 'MEIP', 'OREX', 'POZN', 'PTX', 'SCLN', 'SCMP', 'SGYP', 'UTHR', 'PRGO', 'USNA', 'GNC', 'RAD', 'WBA', 'ABT', 'ADMS', 'AKRX', 'APH', 'BLT', 'CVT', 'FCSC', 'FLXN', 'GALT', 'HZNP', 'IRWD', 'KPTI', 'LCI', 'MDCO', 'MNK', 'MNTA', 'MYL', 'NATR', 'NBIX', 'NU', 'PCRX', 'RIGL', 'ROSE', 'SGNT', 'STAR', 'SUPN', 'TTPH', 'VSAR', 'ZTS', 'ABC', 'CAH', 'MCK', 'AET', 'ANTM', 'CI', 'CNC', 'CVS', 'ESRX', 'HIIQ', 'HUM', 'MGLN', 'MOH', 'UAM', 'UNH', 'WCG', 'ANH', 'BRC', 'CHH', 'CYH', 'HCA', 'LPNT', 'MED', 'NHC', 'SEM', 'THC', 'UHS', 'USMD', 'ACC', 'BKD', 'CSU', 'ENSG', 'FVE', 'KND', 'MET', 'REG', 'ABMD', 'ACRX', 'ADI', 'ALGN', 'AMT', 'ARAY', 'AXP', 'BABY', 'BIO', 'BSX', 'CNMD', 'COH', 'CRY', 'CSII', 'CUTR', 'CYBX', 'CYNO', 'ELX', 'EW', 'EXAC', 'GB', 'GME', 'GMED', 'GNMK', 'HOLX', 'IMI', 'ISRG', 'IVC', 'KTWO', 'LDRH', 'MASI', 'MDT', 'MDXG', 'NUVA', 'NXTM', 'OFIX', 'PHM', 'PHMD', 'RHT', 'RMD', 'RTIX', 'SIRO', 'SN', 'SPNC', 'STE', 'STJ', 'SUN', 'SYK', 'VAR', 'VASC', 'WMGI', 'ZBH', 'ZLTQ', 'ZMH', 'HSIC', 'OMI', 'PBH', 'PDCO', 'PGC', 'PMC', 'AKR', 'AMP', 'ANGO', 'ANN', 'ATEC', 'ATRC', 'ATRI', 'ATRS', 'BAX', 'BCR', 'BDX', 'BIOL', 'CMN', 'CMP', 'COO', 'DSCI', 'ELGX', 'HAE', 'HBIO', 'HRC', 'HTWR', 'IART', 'ICUI', 'IM', 'INGN', 'LMNX', 'MLAB', 'MMSI', 'MTD', 'OSUR', 'PM', 'PODD', 'SFL', 'STAA', 'TFX', 'THOR', 'TNDM', 'TRIV', 'TRNX', 'UNIS', 'UNS', 'UTMD', 'WAT', 'WST', 'XRAY', 'A', 'ABAX', 'AIQ', 'ALOG', 'ALR', 'AXDX', 'BEAT', 'BRKR', 'BRLI', 'COG', 'COV', 'CRL', 'DGX', 'DXCM', 'ENZ', 'EXAS', 'FLDM', 'FMI', 'GES', 'GHDX', 'LH', 'MBI', 'NEO', 'NSPH', 'PEB', 'PKI', 'PRXL', 'Q', 'RDNT', 'SSI', 'TEAR', 'TMO', 'ACHC', 'AMSG', 'DVA', 'HLS', 'HWAY', 'IPCM', 'MD', 'PAHC', 'PRSC', 'USPH', 'AAT', 'AGM', 'ALB', 'AMRS', 'CBT', 'CHMT', 'FOE', 'FUL', 'GPRE', 'GRA', 'HWKN', 'IFF', 'IOSP', 'IPHS', 'KMG', 'KOP', 'KRA', 'KRO', 'KWR', 'LYB', 'NEU', 'ODC', 'OLN', 'OMN', 'ORI', 'POL', 'PPG', 'RPM', 'SHW', 'SIAL', 'SNMX', 'SXT', 'SZYM', 'VAL', 'WDFC', 'WLK', 'AXLL']
