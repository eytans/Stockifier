import pymongo
import argparse
import pandas as pd
import numpy as np
from Utilities.data_orginizers import LearningData


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    args = parser.parse_args()

    # need to be carefull as not all data is initialised
    ld = LearningData(database=args.database)
    market_names = ld.stocks.distinct('market_name')
    market_to_stocks = {m: [] for m in market_names}
    for stock in ld.get_stock_names():
        m = ld.stocks.find_one({'ticker': stock})['market_name']
        market_to_stocks[m].append(stock)

    for market in market_names:
        stocks_data = [(s_name, ld.get_stock_data(s_name, force=False)) for s_name in market_to_stocks[market]]
        market_data = pd.DataFrame(columns=stocks_data[0][1].columns)
        for s_name, s in stocks_data:
            market_data = pd.merge(market_data, s, how='outer', suffixes=('', '_' + s_name), left_index=True, right_index=True)

        docs = {}
        for row in market_data.iterrows():
            date = row[0]
            row = row[1]
            doc = {'market_name': market, 'date': date}
            if date in docs:
                doc = docs[date]
            else:
                doc['size'] = 0
                doc['volume'] = 0
                doc['change'] = 0
            for s_name in market_to_stocks[market]:
                if np.isnan(row['volume_' + s_name]):
                    continue
                try:
                    doc['change'] += (row['close_' + s_name] - row['open_' + s_name]) * row['volume_' + s_name]
                except:
                    continue
                doc['volume'] += row['volume_' + s_name]
                doc['size'] += 1
            if date not in docs:
                ld.markets.insert_one(doc)
            else:
                ld.markets.update_one({'date': doc['date']}, {'$set': {'change': doc['change'], 'volume': doc['volume'],
                                                                       'size': doc['size']}})
            docs[date] = doc


if __name__ == '__main__':
    main()
