import urllib.request
import json
import os
import csv
url = "https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=33sPyUqFDG_3Bjnt3mCy&ticker="
symbolFile = open("symbols.txt", 'r')
#csv_data = open(r'C:\Users\sdshw\Desktop\Stockfier\WIKI_PRICES_212b326a081eacca455e13140d7bb9db\csv_data.csv','r',encoding="utf8")
for stockline in symbolFile.readlines():
    industry, key= stockline.split('=')
    key = str(key).split('-s')
    clean_keys = []
    if not os.path.exists(industry):
        os.makedirs(industry)
    for k in key:
        k = k.strip(' \n\t')
        k = k.split('.')[0]
        if k == '': continue
        clean_keys.append(k)
    count=0
    for k in clean_keys:
        new_url=url+k
        req = urllib.request.Request(url=new_url)
        f = urllib.request.urlopen(req)
        lines = f.read().decode('utf-8')
        js = json.loads(lines)
        if len(js['datatable']['data']) != 0:
            with open(industry+'/'+k+'.csv', 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',lineterminator='\n')
                for ln in js['datatable']['data']:
                    writer.writerow(ln)
                count += 1
    print(industry+': '+str(count))

# Diagnostic Substances (Healthcare): 7
# Hospitals (Healthcare): 12
# Health Care Plans (Healthcare): 16
# Drug Stores (Services): 3
# Medical Instruments & Supplies (Healthcare): 46
# Medical Practitioners (Healthcare): 0
# Drugs - Generic (Healthcare): 31
# Synthetics (Basic Materials): 1
# Medical Equipment Wholesale (Services): 8
# Drugs Wholesale (Services): 3
# Drug Delivery (Healthcare): 4
# Drug Related Products (Healthcare): 2
# Drug Manufacturers - Major (Healthcare): 32
# Specialized Health Services (Healthcare): 11
# Medical Appliances & Equipment (Healthcare): 60
# Chemicals - Major Diversified (Basic Materials): 22
# Accident & Health Insurance (Financial): 8
# Specialty Chemicals (Basic Materials): 39
# Long-Term Care Facilities (Healthcare): 9
# Medical Laboratories & Research (Healthcare): 33
# Drug Manufacturers - Other (Healthcare): 12