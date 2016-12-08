import os
project_dir = os.path.dirname(os.path.dirname(__file__))
utilities_dir = os.path.dirname(__file__)
default_pickle = os.path.join(project_dir, 'learning_data.pickle')


def stock_history_field(day, field=''):
    return field+str(day)+'_days_before'


def market_history_field(day, field=''):
    return field+'markets_'+str(day)+'_days_before'

