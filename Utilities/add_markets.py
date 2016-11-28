import pymongo
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    args = parser.parse_args()

    client = pymongo.MongoClient()
    db = client.get_database(args.database)
    markets = db['markets']

    stats = {}
    col = db['stocks']
    for doc in col.find({}):
        if doc["market_name"] not in stats:
            stats[doc["market_name"]] = {}
        if doc["date"] not in stats[doc["market_name"]]:
            stats[doc["market_name"]][doc["date"]] = {'size': 0, 'volume': 0, 'value': 0}
            stats[doc["market_name"]][doc["date"]]['date'] = doc["date"]
            stats[doc["market_name"]][doc["date"]]['market_name'] = doc["market_name"]
        current = stats[doc["market_name"]][doc["date"]]
        current["size"] += 1
        try:
            current["volume"] += doc["volume"]
        except:
            pass
        try:
            current["close"] += doc["close"]  # sum of closed
        except:
            pass
        try:
            current["open"] += doc["open"]  # sum of closed
        except:
            pass

    for key, val in stats.items():
        for key2, doc in val.items():
            markets.insert_one(doc)


if __name__ == '__main__':
    main()
