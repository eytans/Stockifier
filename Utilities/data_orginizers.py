import pymongo


# receive a sample dictionary
# return a function which akes a dictionary and returns values in a sorted list
def dictionary_sorter(sample):
    keys = list(sample.keys())
    keys.sort()
    sorting_dict = {key: i for i, key in enumerate(keys)}

    def dict_to_sorted_vals(dict):
        vals = [0]*len(keys)
        for k in keys:
            vals[sorting_dict[k]] = dict[k]
        return vals

    return dict_to_sorted_vals


# legal markets is a list of all markets to take or non for all markets
def retreive_daily_markets_data(database='exchange', legal_markets=None):
    client = pymongo.MongoClient()
    db = client[database]
    cl = db['markets']
    search_doc = {}
    if legal_markets:
        search_doc['market_name'] = {'$in': legal_markets}
    curs = cl.find().sort({'intdate': 1})
    data = []
    new = None
    for c in curs:
        if not new:
            new = [c]
        elif c['intdate'] == new[0]['intdate']:
            new.append(c)
        else:
            new.sort(key=lambda doc: doc['market_name'])
            data.append(new)
            new = None
    if new:
        new.sort(key=lambda doc: doc['market_name'])
        data.append(new)
    market_sorter = dictionary_sorter(data[0][0])
    return [[market_sorter(m) for m in day] for day in data]
