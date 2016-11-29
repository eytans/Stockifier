from unittest import TestCase
import pymongo
from Classifiers import classifiers
from sklearn.model_selection import cross_val_score
from functools import reduce


class TestTrain_stock(TestCase):
    def test_train_stock(self):
        client = pymongo.MongoClient()
        db = client['exchange']
        stocks = db['stocks']
        clf = classifiers.train_stock(stocks.find(
            {'ticker': 'NEO'}, {'ticker': 0, '_id': 0, 'market_name': 0, 'date': 0}))
        self.assertIsNotNone(clf)
        data, results = classifiers.get_data_and_results_from_stock(stocks.find({'ticker': 'NEO'},
                                                           {'ticker': 0, '_id': 0, 'market_name': 0, 'date': 0}))
        cros_score = cross_val_score(clf, data, results)
        print(cros_score)
        self.assertGreater(reduce(lambda x, y: x + y, cros_score) / len(cros_score), 0.5)


