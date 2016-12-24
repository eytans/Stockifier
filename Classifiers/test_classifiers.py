from Classifiers.classifiers import create_quarter_clusterer, create_adaboost
from Utilities.orginizers import LearningData
from unittest import TestCase
from sklearn.model_selection import KFold
import Utilities
import logging


class Test_classifiers(TestCase):
    def setUp(self):
        logging.getLogger().setLevel(logging.DEBUG)
        self.ld = LearningData()

    def test_create_quarter_clusterer(self):
        clusterer = create_quarter_clusterer(LearningData(), ['AMRS', 'ALOG', 'AMT', 'BXP', 'CHH'])
        self.assertIsNotNone(clusterer)

    def test_simple_adaboost(self):
        clf = create_adaboost('ABC')
        self.assertIsNotNone(clf)

    def test_adaboost_acc(self):
        stock_name = 'GMED'
        group_kfold = KFold(n_splits=5)
        accuracies = []
        clf, data, classes = create_adaboost(stock_name, return_data=True)
        for train_index, test_index in group_kfold.split(data):
            clf = create_adaboost(stock_name, data=data.iloc[train_index[0]:train_index[-1]].drop('change', axis=1))
            temp = data.iloc[test_index[0]:test_index[-1]].drop('change', axis=1)
            temp_c = classes[test_index[0]:test_index[-1]]
            count = 0
            for d, c in zip(temp.iterrows(), temp_c):
                count += clf.predict(d[1]) == c
            accuracies.append(float(count)/len(temp_c))
        acc = sum(accuracies)/len(accuracies)
        print(acc)
        self.assertGreaterEqual(acc, 0.75)

