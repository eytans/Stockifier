from Classifiers import create_quarter_clusterer, create_adaboost
from Utilities.orginizers import LearningData, TrainingData
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
        clusterer = create_quarter_clusterer(LearningData())
        self.assertIsNotNone(clusterer)

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
        data, classes = TrainingData(stock_name, 3).add_history(10).get()
        data.drop('change', axis=1, inplace=True)
        for train_indices, test_indices in group_kfold.split(data):
            train_data = data.loc[data.index[train_indices]]
            train_classes = classes.loc[classes.index[train_indices]]
            clf = create_adaboost(train_data, train_classes, base_estimator=model)
            temp = data.loc[data.index[test_indices]]
            temp_c = classes.loc[classes.index[test_indices]]
            accuracies.append(clf.score(temp, temp_c))
        acc = sum(accuracies)/len(accuracies)
        print("avarage {} accuracy for {} runs".format(acc, len(accuracies)))
        threshold = classes.value_counts()[True] / len(classes)
        print("threshold is {}".format(threshold))
        print("error reduction was: {}".format(acc - threshold))
        self.assertGreaterEqual(acc, 0.75)

    def test_ready_training_data(self):
        self.assertIsNotNone(TrainingData('ISIS').get())

