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
