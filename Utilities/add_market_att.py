import pymongo
import os
import argparse
import csv
import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    args = parser.parse_args()

    client = pymongo.MongoClient()
    db = client.get_database(args.database)
    cl = db['stocks']
    markets = db['markets']

    data = {}
    cursor = cl.aggregate([{'$group': {
        '_id': {'date': "$date", "market_name": "$market_name"}, 'change': {"$avg": "$change"}
    }}])
    for group_data in cursor:
        data[(group_data['_id']['market_name'], group_data['_id']['date'])] = group_data

    for group_data in data.values():
        markets.update_one(filter={'market_name': group_data['_id']['market_name'], 'date': group_data['_id']['date']},
                       update={"$set": {"change": group_data['change']}})


if __name__ == '__main__':
    main()
