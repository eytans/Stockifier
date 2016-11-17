import pymongo
import argparse
import multiprocessing
from functools import partial


class DateManipulator(object):
    def __init__(self, db):
        self.db = db
        self.stocks_collection = db['stocks']
        self.markets_collection = db['markets']

    # def find_maximal_for_stock_and_market(self, path_to_stock,path_to_market):
    #     first,last = self.maximal_shared_range_dir(path_to_market)
    #     stock_file = open(path_to_stock,'r')
    #     list_of_all_dates = []
    #     for line in stock_file.readlines():
    #         list_of_all_dates.append(line.split(',')[1])
    #     if first < self.getdate(list_of_all_dates[0]):
    #         first = self.getdate(list_of_all_dates[0])
    #     if last > self.getdate(list_of_all_dates[len(list_of_all_dates)-1]):
    #         last = self.getdate(list_of_all_dates[len(list_of_all_dates)-1])
    #     return first, last
    #
    # def summerize_market_size_per_date(self, data_list):
    #     open_size,close_size = 0,0
    #     for line in data_list:
    #         open_size+=float(line.split(',')[2])
    #         close_size+=float(line.split(',')[5])
    #     if open_size > close_size:
    #         return False
    #     else:
    #         return True

    def find_abs_relation(self, stock):
        # check paths
        stock_list = self.stocks_collection.find({'ticker': stock})
        market_to_len = {}
        market_to_succes = {}
        for day in stock_list:
            markets_data = self.markets_collection.find({'date': day['date']})
            daily_change = day['change']
            for m_day in markets_data:
                m_name = m_day['market_name']
                if m_name not in market_to_len:
                    market_to_len[m_name] = 0
                    market_to_succes[m_name] = 0
                market_to_len[m_name] += 1
                market_trend = m_day['change']
                if abs(market_trend-daily_change) < 0.009:
                    market_to_succes[m_name] += 1
        return {key: market_to_succes[key]/market_to_len[key] for key in market_to_succes.keys()}

    # def main_relation_classifier(self, stock_path,market_path):
    #     # check paths
    #     first_date,last_date = self.find_maximal_for_stock_and_market(stock_path,market_path)
    #     market_dic = self.get_relevant_data_market(first_date,last_date,market_path)
    #     stock_list = self.get_relevant_data_stock(first_date,last_date,stock_path)
    #     data_length = len(stock_list)-1
    #     success_count = 0
    #     for day in stock_list:
    #         if day.split(',')[2] > day.split(',')[5]:
    #             day_trend = False
    #         else:
    #             day_trend = True
    #         try:
    #             market_trend = self.summerize_market_size_per_date(market_dic[day.split(',')[1]])
    #         except:
    #             continue
    #         if market_trend==day_trend:
    #             success_count+=1
    #     return success_count/data_length


market_list = ['Accident & Health Insurance (Financial)','Chemicals - Major Diversified (Basic Materials)',
               'Diagnostic Substances (Healthcare)','Drug Delivery (Healthcare)','Drug Manufacturers - Other (Healthcare)',
               'Drug Related Products (Healthcare)','Drug Stores (Services)',
               'Drugs Wholesale (Services)','Health Care Plans (Healthcare)',
               'Hospitals (Healthcare)','Long-Term Care Facilities (Healthcare)','Medical Equipment Wholesale (Services)',
               'Medical Instruments & Supplies (Healthcare)','Medical Laboratories & Research (Healthcare)',
               'Specialized Health Services (Healthcare)','Specialty Chemicals (Basic Materials)',
               'Synthetics (Basic Materials)']
# print(self.find_shared_max_interval(path1,path2))
# start,finish = maximal_shared_range_dir(path3)
# print(get_relevant_data(start, finish, path3))
# print(find_maximal_for_stock_and_market(path4,path3))

# TODO problem with drug manufactor major & drugs generics & Medical Appliances & Equipment (Healthcare)


# stock_path= sys.argv[1]
# market_path = sys.argv[2]
def work_on_it(db_name, stock):
    client = pymongo.MongoClient()
    db = client.get_database(db_name)
    relations = DateManipulator(db).find_abs_relation(stock)
    cl = db['metadata']
    cl.update_one(filter={'ticker': stock}, update={'$set': {'relations': relations}}, upsert=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    args = parser.parse_args()

    pool = multiprocessing.Pool()

    db_name = args.database

    client = pymongo.MongoClient()
    db = client.get_database(db_name)
    stocks = db['stocks']
    pool.map(partial(work_on_it, db_name), stocks.distinct(key='ticker'))

if __name__ == '__main__':
    main()
