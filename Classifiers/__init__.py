from Classifiers.classifiers import *
from Utilities.orginizers import LearningData, DataAccessor, TrainingData
from sklearn.tree import DecisionTreeClassifier
import logging
import sklearn
import itertools


def create_adaboost(data, classes, base_estimator=DecisionTreeClassifier()):
    res = sklearn.ensemble.AdaBoostClassifier(base_estimator=base_estimator, n_estimators=200).fit(data, classes)
    return res
