import pymongo


class LearningData(object):
    __market_data = {}
    __stock_data = {}

    class DictionarySorter(object):
        '''Using a sample dictionary create a fast mapping from key to index.
        API include way to get a key for a given index and to create a list from a different dictionary with same keys.
        '''
        def __init__(self, sample):
            keys = list(sample.keys())
            keys.sort()
            self.sorting_dict = {key: i for i, key in enumerate(keys)}

        def __call__(self, d, *args, **kwargs):
            vals = [0] * len(self.sorting_dict)
            for k in d.keys():
                vals[self.sorting_dict[k]] = d[k]
            return vals

        def sort(self, d):
            return self(d)

        def get_index(self, key):
            return self[key]

        def __getitem__(self, item):
            return self.sorting_dict[item]

    def __init__(self, database='exchange', legal_markets=None):
        client = pymongo.MongoClient()
        db = client[database]
        self.database = database
        self.markets = db['markets']
        self.stocks = db['stocks']
        self.legal_markets = legal_markets
        if self.legal_markets is None:
            self.legal_markets = self.markets.distinct('market_name')

        self.market_sorter = LearningData.DictionarySorter(self.markets.find_one())
        self.stock_sorter = LearningData.DictionarySorter(self.stocks.find_one())
        self.stock_data = {}

    def __init_market_data(self):
        if self.database not in LearningData.__market_data:
            LearningData.__market_data[self.database] = {}
            data = LearningData.__market_data[self.database]
            for m in self.markets.find():
                if m['market_name'] not in data:
                    data[m['market_name']] = {}
                data[m['market_name']][m['date']] = m

    def get_market_data(self):
        self.__init_market_data()
        return LearningData.__market_data[self.database]

    def __init_stock_data(self):
        if self.database not in LearningData.__stock_data:
            LearningData.__stock_data[self.database] = {}
            data = LearningData.__stock_data[self.database]
            for doc in self.stocks.find():
                name = doc['ticker']
                if name not in data:
                    data[name] = {}
                data[name][doc['date']] = doc

    def get_stock_data(self, stock_name=None):
        self.__init_stock_data()
        if not stock_name:
            return LearningData.__stock_data[self.database]
        return LearningData.__stock_data[self.database][stock_name]


    def stock_classifier_data(self):
        pass

    def retreive_daily_markets_data(self):
        search_doc = {}
        if legal_markets:
            search_doc['market_name'] = {'$in': legal_markets}
        curs = cl.find(search_doc).sort({'intdate': 1})
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

    def get_stock_ordered_data(self, stock_name, database='exchange'):
        client = pymongo.MongoClient()
        db = client[database]
        cl = db['stocks']
        data = list(cl.find({'ticker': stock_name}).sort({'intdate': 1}))
        stock_sorter = dictionary_sorter(data[0])
        data = [stock_sorter(s) for s in data]
        return data

    def retrieve_stock_data_and_classes(self, stock_name, database='exchange'):
        data = self.get_stock_ordered_data(stock_name, database)
        results = list(map(lambda d: (d['close'] - d['open']) * d['open'] < 0.3, data[1:]))
        data = list(map(lambda d: list(d.values()), data))
        data = data[:-1]
        return data, results
