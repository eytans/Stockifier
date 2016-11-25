import pymongo
import os
import argparse
import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory from which to read all subdirectories')
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    parser.add_argument('-m', '--daymemory', default=7, type='int', help='name of database to connect to')
    args = parser.parse_args()

    client = pymongo.MongoClient()
    db = client.get_database(args.database)
    cl = db['stocks']

    for d in filter(os.path.isdir, map(lambda sd: os.path.join(args.dir, sd), os.listdir(args.dir))):
        market_name = os.path.basename(d)
        for csvf in os.listdir(d):
            cl.update_many(filter={'ticker': os.path.splitext(csvf)[0]}, update={"$set": {"market_name": market_name}})

    dates = cl.distinct(key='date')
    for date in dates:
        intdate = datetime.datetime.strptime(date, '%Y-%m-%d').timestamp()
        cl.update_many(filter={'date': date}, update={"$set": {"intdate": intdate}})

    stock_data = list(cl.find({}))
    stock_data.sort(key=lambda doc: doc['intdata'])
    for i, doc in enumerate(stock_data[args.daymemory:]):
        i += args.daymemory
        for j in range(1, 1+args.daymemory):
            doc[str(j) + '_days_before'] = stock_data[i-j]['_id']


if __name__ == '__main__':
    main()