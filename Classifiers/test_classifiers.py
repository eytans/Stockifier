from Classifiers import create_quarter_clusterer, create_adaboost, ready_training_data
from Utilities.orginizers import LearningData
from unittest import TestCase
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier
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

    def test_tree_adaboost(self):
        self.adaboost_acc(DecisionTreeClassifier())

    def test_logistic_regression_adaboost(self):
        self.adaboost_acc(LogisticRegression())

    def test_svm_adaboost(self):
        self.adaboost_acc(SVC())

    def test_bagging_svm_adaboost(self):
        self.adaboost_acc(BaggingClassifier(SVC(), max_features=0.5, max_samples=0.5))

    def adaboost_acc(self, model):
        stock_name = 'LCI'
        group_kfold = KFold(n_splits=5, shuffle=True)
        accuracies = []
        data, classes = ready_training_data(stock_name, days_forward=3)
        for train_indices, test_indices in group_kfold.split(data):
            train_data = data.loc[data.index[train_indices]].drop('change', axis=1)
            train_classes = classes.loc[classes.index[train_indices]]
            clf = create_adaboost(stock_name, data=train_data, classes=train_classes, days_forward=3,
                                  base_estimator=model)
            temp = data.loc[data.index[test_indices]].drop('change', axis=1)
            temp_c = classes.loc[classes.index[test_indices]]
            accuracies.append(clf.score(temp, temp_c))
        acc = sum(accuracies)/len(accuracies)
        print("avarage {} accuracy for {} runs".format(acc, len(accuracies)))
        threshold = classes.value_counts()[True] / len(classes)
        print("threshold is {}".format(threshold))
        print("error reduction was: {}".format(acc - threshold))
        self.assertGreaterEqual(acc, 0.75)

