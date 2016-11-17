import pymongo
import os
import argparse
import csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory from which to read all subdirectories')
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    parser.add_argument('-f', '--flags', help='which fields to add to database')
    args = parser.parse_args()

    client = pymongo.MongoClient()
    db = client.get_database(args.database)

    names = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'ex-divident', 'split_ratio', 'adj_open',
             'adj_high', 'adj_low', 'adj_close', 'adj_volume']

    for d in filter(os.path.isdir, map(lambda sd: os.path.join(args.dir, sd), os.listdir(args.dir))):
        cl = db['stocks']
        for csvf in os.listdir(d):
            with open(os.path.join(d, csvf), newline='') as f:
                reader = csv.reader(f)
                check_if_new = False
                if cl.count() > 0:
                    check_if_new = True

                for row in reader:
                    doc = {}
                    for i, att in enumerate(names):
                        try:
                            doc[att] = float(row[i])
                        except:
                            doc[att] = row[i]
                    if isinstance(doc['open'], float) and isinstance(doc['close'], float):
                        doc['change'] = abs(doc['open'] - doc['close']) / doc['open']
                    else:
                        doc['change'] = 0

                    if check_if_new:
                        pass

                    cl.insert_one(doc)


if __name__ == '__main__':
    main()