from datetime import date


def find_shared_max_interval(path1,path2):
    """
    Parameters
    ----------
    path1 path2
    Returns
    -------
    both path1&path2 are paths to csv files that contains stocks historical daily data.
    the function will return the maximal common period of both files
    """
    getdate = lambda str_date : date(*map(int, str_date.split('-')))
    file1 = open(path1,'r')
    file2 = open(path2,'r')
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
    print("first common date is " + str(getdate(list2[index2])))
    index1,index2 = len(list1)-1,len(list2)-1
    while getdate(list1[index1])>getdate(list2[index2]):
        index1-=1
        if index1 < 0:
            raise
    while getdate(list2[index2]) > getdate(list1[index1]):
        index2 -= 1
        if index2 < 0:
            raise
    print("last common date is " + str(getdate(list2[index2])))
    first_common = getdate(list2[index2])


    # print(getdate(list1[0])<getdate(list2[0])) bigger is later

path1 = "C:/Users/sdshw/Desktop/Stockfier/stockifier/YahStocks/Accident & Health Insurance (Financial)/AFL.csv"
path2 = "C:/Users/sdshw/Desktop/Stockfier/stockifier/YahStocks/Accident & Health Insurance (Financial)/AIZ.csv"
find_shared_max_interval(path1,path2)