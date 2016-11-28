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
    for stock_name, data in stock_data:
        for date, doc in data:
            for j in range(1, 1 + args.daymemory):
                new_date = date - datetime.timedelta(days=j)
                doc[str(j) + '_days_before'] = None
                if new_date in data:
                    doc[str(j) + '_days_before'] = data[new_date]['_id']
                for market_name in market_data.keys():
                    doc['markets_' + str(j) + '_days_before'] = None
                    if new_date in market_data[market_name]:
                        doc['markets_' + str(j) + '_days_before'] = market_data[market_name][new_date]['_id']
            cl.update_one({'_id': doc['_id']})


if __name__ == '__main__':
    main()