import pymongo
import argparse
import multiprocessing
from functools import partial


class DateManipulator(object):
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
    #        2 open_size+=float(line.split(',')[2])
    #         close_size+=float(line.split(',')[5])
    #     if open_size > close_size:
    #         return False
    #     else:
    #         return True

    def find_abs_relation(self, stock_list, markets):
        # check paths
        market_to_len = {}
        market_to_success = {}
        for day in stock_list:
            markets_data = markets[day['date']]
            daily_change = day['change']
            for m_day in markets_data:
                m_name = m_day['market_name']
                if m_name not in market_to_len:
                    market_to_len[m_name] = 0
                    market_to_success[m_name] = 0
                market_to_len[m_name] += 1
                market_trend = m_day['change']
                if abs(market_trend-daily_change) < 0.009:
                    market_to_success[m_name] += 1
        return {key: market_to_success[key]/market_to_len[key] for key in market_to_success.keys()}

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

market_data = {}
stock_data = {}


# stock_path= sys.argv[1]
# market_path = sys.argv[2]
def work_on_it(stock_data, market_data, db_name,db):
    relations = DateManipulator().find_abs_relation(stock_data, market_data)
    cl = db['metadata']
    cl.update_one(filter={'ticker': stock_data[0]['ticker']}, update={'$set': {'relations': relations}}, upsert=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    args = parser.parse_args()

    pool = multiprocessing.Pool(1)

    db_name = args.database

    client = pymongo.MongoClient()
    db = client.get_database(db_name)
    stocks = db['stocks']
    markets = db['markets']

    for s in stocks.distinct(key='ticker'):
        stock_data[s] = list(stocks.find({'ticker': s}))

    for s in markets.distinct(key='market_name'):
        for row in markets.find({'market_name': s}):
            date = row['date']
            if date not in market_data:
                market_data[date] = []
            market_data[date].append(row)

    client = pymongo.MongoClient()
    db = client.get_database(db_name)
    pool.map(partial(work_on_it, market_data=market_data, db_name=db_name,db=db),
             map(lambda x: stock_data[x], stocks.distinct(key='ticker')))

if __name__ == '__main__':
    main()
