import pymongo
import argparse
import Utilities
from Utilities.data_orginizers import LearningData


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    parser.add_argument('-m', '--daymemory', default=7, type=int, help='name of database to connect to')

    args = parser.parse_args()

    client = pymongo.MongoClient()
    db = client.get_database(args.database)
    cl = db['stocks']

    learning_data = LearningData()
    update = {}
    for j in range(0, args.daymemory):
        update[Utilities.market_history_field(j)] = {}
    cl.update_many(filter={}, update={'$set': update})
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
                update[Utilities.stock_history_field(j)] = stock_prev[j]
                for market_name in market_data.keys():
                    m_prev = market_prev[market_name]
                    if len(m_prev) < j + 1:
                        continue
                    update[Utilities.market_history_field(j)+'.'+market_name] = m_prev[j]

            cl.update_one(filter={'_id': row['_id']}, update={'$set': update})
            stock_prev.insert(0, row['_id'])
            for market_name in market_data.keys():
                market_prev[market_name].insert(0, market_data[market_name].get_value(row.name, '_id'))


if __name__ == '__main__':
    main()
