import sklearn.ensemble
import sklearn.cluster
import sklearn.metrics
from Utilities.orginizers import *
import Utilities
from math import *
import functools
import logging
import itertools
import collections
import numpy as np
from pathos import multiprocessing


# Classifier implementing sklearn standards (for easier cross validation).
# This class creates 3 classifiers from the model, using the relation classifier if provided.
# relation classifier should have fields and strength for each connection
# classification is done using base estimator, strength*connections regularised by combined.
class ConnectionStrengthClassifier(sklearn.base.BaseEstimator):
    def __init__(self, threshold=0.1, base_strength=0.5, combined_weight=0.5, njobs=None, base_estimator=sklearn.tree.DecisionTreeClassifier()):
        """
        :param threshold: minimum value of relations to consider.
        :param combined_weight: the weight to put on the combined classifier.
        :param base_estimator: the estimator to use as a model for the fit.
        """
        self.base_estimator = base_estimator
        self.threshold = threshold
        self.combined_weight = combined_weight
        self.base_strength = base_strength
        self.njobs = njobs

    def fit(self, X, y, connection_columns, strengths):
        """
        :param X: data from which to learn
        :param y: classifications corresponding to @X
        :param connection_columns: a list of lists, each of which is the columns of a specific connection
        :param strengths: strength of a connection corresponding to @connection_columns
        :return: self after learning the given data
        """
        if X.shape[0] != y.shape[0]:
            raise ValueError("number of X rows must be equal to number of y rows.")
        used_cols = set(functools.reduce(lambda t, k: t+k, connection_columns))
        self.base_cols_ = [c for c in X.columns if c not in used_cols]
        self.base_estimator_ = sklearn.base.clone(self.base_estimator).fit(X[self.base_cols_], y)

        self.combined_estimators_ = []
        self.connections_estimators_ = []
        self.relations_ = []
        self.cols_ = []
        if self.njobs != 1:
            pool = multiprocessing.Pool(processes=self.njobs)

        for cols, stren in zip(connection_columns, strengths):
            if stren < self.threshold:
                continue
            cols = [c for c in cols if c in X.columns]
            if len(cols) == 0:
                continue
            self.relations_.append(stren)
            self.cols_.append(cols)

        def train_connection(cols):
            return sklearn.base.clone(self.base_estimator).fit(X[cols], y)

        if self.njobs == 1:
            func = map
        else:
            func = pool.map()
        self.connections_estimators_ = list(func(train_connection, self.cols_))

        def train_combined(cols):
            return sklearn.base.clone(self.base_estimator).fit(X[self.base_cols_ + cols], y)

        self.combined_estimators_ = list(func(train_combined, self.cols_))

        self.classes_ = self.base_estimator_.classes_
        if self.njobs != 1:
            pool.close()
        return self

    def __predict_from_probs(self, probs):
        bp = 0
        bi = 0
        for i, p in enumerate(probs):
            if bp < p:
                bp, bi = p, i
        return self.classes_[bi]

    def predict(self, X):
        predictions = self.predict_proba(X)
        return [self.__predict_from_probs(probs) for probs in predictions]

    def predict_proba(self, X):
        predictions = []
        for combined_e, connection_e, cols in zip(self.combined_estimators_, self.connections_estimators_, self.cols_):
            combined = combined_e.predict_proba(X[self.base_cols_ + cols])
            connect = connection_e.predict_proba(X[cols])
            predictions.append((combined * self.combined_weight) + ((1 - self.combined_weight) * connect))

        # used to be maximum of self.relations_ and 1 we want to test self.realtions_
        base = [self.base_strength * p for p in self.base_estimator_.predict_proba(X[self.base_cols_])]
        results = []
        for rel, probs in zip(self.relations_, predictions):
            results.append([b + p * rel for b, p in zip(base, probs)])
        return functools.reduce(lambda x, y: [x1 + y1 for x1, y1 in zip(x, y)], results)

    def score(self, X, y):
        return sklearn.metrics.accuracy_score(y, self.predict(X))