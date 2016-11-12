import pymongo
import os
import argparse
import csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory from which to read all subdirectories')
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    args = parser.parse_args()

    client = pymongo.MongoClient()
    db = client.get_database(args.database)
    cl = db['stocks']

    for d in filter(os.path.isdir, map(lambda sd: os.path.join(args.dir, sd), os.listdir(args.dir))):
        market_name = os.path.basename(d)
        for csvf in os.listdir(d):
            cl.update_many(filter={'ticker': os.path.splitext(csvf)[0]}, update={"$set": {"market_name": market_name}})


if __name__ == '__main__':
    main()