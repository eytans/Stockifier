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

    market_names = db['markets'].distinct('market_name')

    learning_data = LearningData()
    market_data = learning_data.get_market_data()

    for stock_name in learning_data.get_stock_names():
        data = learning_data.get_stock_data(stock_name)
        stock_prev = []
        market_prev = {market_name: [] for market_name in market_names}
        for date, row in data.iterrows():
            update = {}
            for j in range(1, args.daymemory):
                if len(stock_prev) < j + 1:
                    continue
                update[Utilities.stock_history_field(j)] = stock_prev[j]
                for market_name in market_names:
                    m_prev = market_prev[market_name]
                    if len(m_prev) < j + 1:
                        continue
                    update[Utilities.market_history_field(j, market_name)] = m_prev[j]
            if update:
                cl.update_one(filter={'_id': row['_id']}, update={'$set': update})
            stock_prev.insert(0, row['_id'])
            if len(stock_prev) > args.daymemory:
                stock_prev.pop()
            for market_name in market_names:
                m_prev = market_prev[market_name]
                val = Utilities.dataframe_safe_get_value(market_data[market_name], row.name, '_id')
                if val:
                    m_prev.insert(0, val)
                if len(m_prev) > args.daymemory:
                    m_prev.pop()


if __name__ == '__main__':
    main()
