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
        stock_name = 'LCI'
        group_kfold = KFold(n_splits=5, shuffle=True)
        accuracies = []
        clf, data, classes = create_adaboost(stock_name, return_data=True, days_forward=3)
        for train_indices, test_indices in group_kfold.split(data):
            train_data = data.loc[data.index[train_indices]].drop('change', axis=1)
            clf = create_adaboost(stock_name, data=train_data, days_forward=3)
            temp = data.loc[data.index[test_indices]].drop('change', axis=1)
            temp_c = classes.loc[data.index[test_indices]]
            count = 0
            for d, c in zip(temp.iterrows(), temp_c):
                count += clf.predict(d[1]) == c
            accuracies.append(float(count)/len(test_indices))
        acc = sum(accuracies)/len(accuracies)
        print("avarage {} accuracy for {} runs".format(acc, len(accuracies)))
        threshold = classes.value_counts()[True] / len(classes)
        print("threshold is {}".format(threshold))
        print("error reduction was: {}".format(acc - threshold))
        self.assertGreaterEqual(acc, 0.75)

