import pymongo
import os
import argparse
from Utilities.data_orginizers import LearningData
import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    parser.add_argument('-m', '--daymemory', default=7, type=int, help='name of database to connect to')

    args = parser.parse_args()

    client = pymongo.MongoClient()
    db = client.get_database(args.database)
    cl = db['stocks']

    learning_data = LearningData()
    market_data = learning_data.get_market_data()
    stock_data = learning_data.get_stock_data()
    for stock_name, data in stock_data.items():
        stock_prev = []
        market_prev = {market_name: [] for market_name in market_data.keys()}
        for date, row in data.iterrows():
            update = {}
            for j in range(0, args.daymemory):
                if len(stock_prev) < j + 1:
                    continue
                update[str(j) + '_days_before'] = stock_prev[j]
                update['markets_' + str(j) + '_days_before'] = {}
                for market_name in market_data.keys():
                    m_prev = market_prev[market_name]
                    if len(m_prev) < j + 1:
                        continue
                    update['markets_' + str(j) + '_days_before'][market_name] = m_prev[j]
            if update:
                cl.update_one(filter={'_id': row['_id']}, update={'$set': update})
            stock_prev.insert(0, row['_id'])
            for market_name in market_data.keys():
                market_prev[market_name].insert(0, market_data[market_name].get_value(row.name, '_id'))


if __name__ == '__main__':
    main()
