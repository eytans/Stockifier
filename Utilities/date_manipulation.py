from datetime import date
import os
import sys
import pymongo
import os
import argparse
import csv


def getdate(str_date):
    date(*map(int, str_date.split('-')))


def find_shared_max_interval(path1, path2):
    """
    Parameters
    ----------
    path1 path2
    Returns
    -------
    both path1&path2 are paths to csv files that contains stocks historical daily data.
    the function will return the maximal common period of both files
    """
#    getdate = lambda str_date : date(*map(int, str_date.split('-')))
    file1 = open(path1, 'r')
    file2 = open(path2, 'r')
    list1 = []
    list2 = []
    for line in file1.readlines():
        list1.append(line.split(',')[1])
    for line in file2.readlines():
        list2.append(line.split(',')[1])
    index1,index2 = 0,0
    while getdate(list1[index1])>getdate(list2[index2]):
        index2+=1
        if index2 > len(list2)-1:
            raise
    while getdate(list2[index2]) > getdate(list1[index1]):
        index1 += 1
        if index1 > len(list1) - 1:
            raise
    #print("first common date is " + str(getdate(list2[index2])))
    first_common = getdate(list2[index2])
    index1,index2 = len(list1)-1,len(list2)-1
    while getdate(list1[index1])>getdate(list2[index2]):
        index1-=1
        if index1 < 0:
            raise
    while getdate(list2[index2]) > getdate(list1[index1]):
        index2 -= 1
        if index2 < 0:
            raise
    #print("last common date is " + str(getdate(list2[index2])))
    last_common = getdate(list2[index2])
    return first_common,last_common


def maximal_shared_range_dir(path):
    #check that the path exists
    if not os.path.isdir(path):
        print("Invalid path")
        return
    all_files = os.listdir(path)
    min_date, max_date = None,None
    for f in all_files:
        list_of_dates = []
        file1 = open(path + '/' + f)
        for line in file1.readlines():
            list_of_dates.append(line.split(',')[1])
        if min_date is None:
            min_date = getdate(list_of_dates[0])
        if max_date is None:
            max_date = getdate(list_of_dates[len(list_of_dates)-1])
        if min_date < getdate(list_of_dates[0]):
            min_date = getdate(list_of_dates[0])
        if max_date > getdate(list_of_dates[len(list_of_dates)-1]):
            max_date = getdate(list_of_dates[len(list_of_dates)-1])
    return min_date, max_date


def get_relevant_data_market(start_date,finish_date,path):
    """

    Parameters
    ----------
    start_date
    finish_date
    path

    Returns
    -------
    a dictionary that contains all relevant data from a dir between given dates
    """
    if finish_date<start_date:
        print(path)
        raise
    if not os.path.isdir(path):
        raise
    all_files = os.listdir(path)
    first_file = open(path+'/'+all_files[0])
    list_of_dates = []
    for line in first_file.readlines():
        if getdate(line.split(',')[1]) >= start_date and getdate(line.split(',')[1]) <= finish_date:
            list_of_dates.append(line.split(',')[1])
    relevant_data = {key: [] for key in list_of_dates}
    for f in all_files:
        file = open(path+'/'+f)
        for line in file.readlines():
            if line.split(',')[1] not in list_of_dates:
                continue
            else:
                relevant_data[line.split(',')[1]].append(line)
    return relevant_data

def get_relevant_data_stock(start_date,finish_date,path):
    """

    Parameters
    ----------
    start_date
    finish_date
    path

    Returns
    -------
    returns a list that contains all relevant lines from the stock data file
    """
    if finish_date<start_date:
        raise
    if not os.path.isfile(path):
        raise
    first_file = open(path,'r')
    list_of_data = []
    for line in first_file.readlines():
        if getdate(line.split(',')[1]) >= start_date and getdate(line.split(',')[1]) <= finish_date:
            list_of_data.append(line)
    return list_of_data


def find_maximal_for_stock_and_market(path_to_stock,path_to_market):
    first,last = maximal_shared_range_dir(path_to_market)
    stock_file = open(path_to_stock,'r')
    list_of_all_dates = []
    for line in stock_file.readlines():
        list_of_all_dates.append(line.split(',')[1])
    if first < getdate(list_of_all_dates[0]):
        first = getdate(list_of_all_dates[0])
    if last > getdate(list_of_all_dates[len(list_of_all_dates)-1]):
        last = getdate(list_of_all_dates[len(list_of_all_dates)-1])
    return first, last

def summerize_market_size_per_date(data_list):
    open_size,close_size = 0,0
    for line in data_list:
        open_size+=float(line.split(',')[2])
        close_size+=float(line.split(',')[5])
    if open_size > close_size:
        return False
    else:
        return True

def summerize_market_change_per_date(data_list):
    open_size,close_size = 0,0
    for line in data_list:
        open_size+=float(line.split(',')[2])
        close_size+=float(line.split(',')[5])
    return abs((open_size - close_size) / open_size)

def find_abs_relation(stock_path,market_path):
    # check paths
    first_date,last_date = find_maximal_for_stock_and_market(stock_path,market_path)
    market_dic = get_relevant_data_market(first_date,last_date,market_path)
    stock_list = get_relevant_data_stock(first_date,last_date,stock_path)
    data_length = len(stock_list)-1
    success_count = 0
    for day in stock_list:
        daily_change = abs(float(day.split(',')[2]) - float(day.split(',')[5])) / float(day.split(',')[2])
        try:
            market_trend = summerize_market_change_per_date(market_dic[day.split(',')[1]])
        except:
            continue
        if abs(market_trend-daily_change)<0.009:
            success_count+=1
    return success_count/data_length

def main_relation_classifier(stock_path,market_path):
    # check paths
    first_date,last_date = find_maximal_for_stock_and_market(stock_path,market_path)
    market_dic = get_relevant_data_market(first_date,last_date,market_path)
    stock_list = get_relevant_data_stock(first_date,last_date,stock_path)
    data_length = len(stock_list)-1
    success_count = 0
    for day in stock_list:
        if day.split(',')[2] > day.split(',')[5]:
            day_trend = False
        else:
            day_trend = True
        try:
            market_trend = summerize_market_size_per_date(market_dic[day.split(',')[1]])
        except:
            continue
        if market_trend==day_trend:
            success_count+=1
    return success_count/data_length


market_list = ['Accident & Health Insurance (Financial)','Chemicals - Major Diversified (Basic Materials)',
               'Diagnostic Substances (Healthcare)','Drug Delivery (Healthcare)','Drug Manufacturers - Other (Healthcare)',
               'Drug Related Products (Healthcare)','Drug Stores (Services)',
               'Drugs Wholesale (Services)','Health Care Plans (Healthcare)',
               'Hospitals (Healthcare)','Long-Term Care Facilities (Healthcare)','Medical Equipment Wholesale (Services)',
               'Medical Instruments & Supplies (Healthcare)','Medical Laboratories & Research (Healthcare)',
               'Specialized Health Services (Healthcare)','Specialty Chemicals (Basic Materials)',
               'Synthetics (Basic Materials)']
# print(find_shared_max_interval(path1,path2))
# start,finish = maximal_shared_range_dir(path3)
# print(get_relevant_data(start, finish, path3))
# print(find_maximal_for_stock_and_market(path4,path3))

# TODO problem with drug manufactor major & drugs generics & Medical Appliances & Equipment (Healthcare)


# stock_path= sys.argv[1]
# market_path = sys.argv[2]
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory from which to read all subdirectories')
    parser.add_argument('stockcsv', help='path to file to use for relations')
    parser.add_argument('-d', '--database', default='exchange', help='name of database to connect to')
    args = parser.parse_args()

    client = pymongo.MongoClient()
    db = client.get_database(args.database)
    cl = db['metadata']

    stock_name = os.path.splitext(os.path.basename(args.stockcsv))[0]
    relations = {}
    for market in market_list:
        relations[market] = find_abs_relation(args.stockcsv, os.path.join(args.dir+market))
    cl.update_one(filter={'stock': stock_name}, update={'$set': {'relations': relations}})

if __name__ == '__main__':
    main()
