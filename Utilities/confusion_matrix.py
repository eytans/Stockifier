import pandas
import copy
from sklearn.metrics import confusion_matrix
import numpy
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
import sklearn.metrics
from functools import lru_cache

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


class PrecisionRecallSampler(object):
    def __init__(self, x, y, range=2, jump=0.2):
        self.range = range
        self.jump = jump
        self.x = x
        self.y = y

    @lru_cache()
    def get(self, model, **kwargs):
        m = sklearn.clone(model)
        precisions = []
        recalls = []
        cur = self.jump
        while cur <= self.range:
            m.set_params(**{"class_weight": cur})
            cur += self.jump
            cm = ConfusionMatrix((self.x, self.y), m, **kwargs)
            precisions.append(cm.TruePos/(cm.TruePos+cm.FalsePos))
            recalls.append(cm.TruePos/(cm.TruePos+cm.FalseNeg))
        return precisions, recalls

class ConfusionMatrix(object):
    def __init__(self, stock, model, strength=None, connections=None):
        #print("27")
        d, c = stock
        self.data, self.classes = stock
        self.models = model
        self.strength = strength
        self.connections = connections
        self.cnf_matrix = numpy.zeros((2, 2))
        self.accuracy = 0
        self.normalize = []
        self.model = model
        self.TruePos = 0
        self.TrueNeg = 0
        self.FalsePos = 0
        self.FalseNeg = 0
        self.calc_mat()

    def __repr__(self):
        st = ""
        st += str(self.models)
        st += ("\nAccuracy: "+str(self.accuracy))
        return st

    def __str__(self):
        return self.__repr__()

    def true_acc(self):
        return self.TruePos / (self.TruePos + self.FalsePos)

    def false_acc(self):
        return self.TrueNeg / (self.TrueNeg + self.FalseNeg)

    @staticmethod
    def concat(*args, iterator=None):
        it = args
        if iterator is not None:
            it = iterator

        data = list(it)
        res = copy.deepcopy(data[0])
        res.accuracy = mean([d.accuracy for d in data])
        res.TruePos = mean([d.TruePos for d in data])
        res.TrueNeg = mean([d.TrueNeg for d in data])
        res.FalsePos = mean([d.FalsePos for d in data])
        res.FalseNeg = mean([d.FalseNeg for d in data])
        return res

    def calc_mat(self):
        tmp_accuracy = 0
        # (d.iloc[0:round(len(d) * 0.7)], c.iloc[0:round(len(d) * 0.7)])
        # self.test_data = (d.iloc[round(len(d) * 0.7):len(d) - 1], c.iloc[round(len(d) * 0.7):len(d) - 1])
        for train_indexes, test_indexes in KFold().split(self.data):
            d, c = self.data.iloc[train_indexes], self.classes.iloc[train_indexes]
            td, tc = self.data.iloc[test_indexes], self.classes.iloc[test_indexes]
            if (self.strength is not None) and (self.connections is not None):
                y_pred = self.models.fit(d, c, self.connections, self.strength).predict(td)
            else:
                y_pred = self.models.fit(d, c).predict(td)
            self.cnf_matrix += confusion_matrix(tc, y_pred)
            tmp_accuracy += sklearn.metrics.accuracy_score(tc, y_pred, normalize=True)
        self.__mean_matrix()
        self.accuracy = tmp_accuracy/3
        return self.normalize

    def __mean_matrix(self):
        c = self.cnf_matrix / 3
        total = c[0][0] + c[0][1] + c[1][0] + c[1][1]
        d = c/total
        self.TrueNeg = d[0][0]
        self.FalseNeg = d[1][0]
        self.FalsePos = d[0][1]
        self.TruePos = d[1][1]
        self.normalize = d
        return d

    def plot(self):
        print(self.models)
        print("Accuracy: "+str(self.accuracy))
        columns = ['Predicted Positive', 'Predicted Negative']
        rows = ['Actual Positive', 'Actual Negative']
        cells = [[str(self.TruePos),str(self.FalseNeg)],[str(self.FalsePos),str(self.TrueNeg)]]
        fig, axs = plt.subplots(1, 1)
        the_table = axs.table(cellText=cells, rowLabels=rows, colLabels=columns, loc='center')
        axs.axis('tight')
        axs.axis('off')
        the_table.set_fontsize(24)
        the_table.scale(2, 2)
        plt.show()
