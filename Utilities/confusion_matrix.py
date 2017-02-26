import pandas
import copy
from sklearn.metrics import confusion_matrix
import numpy
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
import sklearn.metrics

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


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
        return self.TruePos / (self.TruePos + self.TrueNeg)

    def false_acc(self):
        return self.FalsePos / (self.FalsePos + self.FalseNeg)

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
            self.cnf_matrix += self.__normalize_rearrange_matrix(confusion_matrix(tc, y_pred))
            tmp_accuracy += sklearn.metrics.accuracy_score(tc, y_pred, normalize=True)
        self.__mean_matrix()
        self.accuracy = tmp_accuracy/3
        return self.normalize

    def __normalize_matrix(self):
        d = numpy.zeros((2, 2))
        c = self.cnf_matrix
        total = c[1][0] + c[0][0] + c[1][1] + c[0][1]
        d[1][1] = c[0][0] / total
        self.TrueNeg = d[1][1]
        d[0][1] = c[1][0] / total
        self.FalseNeg = d[0][1]
        d[1][0] = c[0][1] / total
        self.FalsePos = d[1][0]
        d[0][0] = c[1][1] / total
        self.TruePos = d[0][0]
        self.normalize = d
        return d

    def __mean_matrix(self):
        d = numpy.zeros((2, 2))
        c = self.cnf_matrix
        d[1][1] = c[1][1] / 3
        self.TrueNeg = d[1][1]
        d[0][1] = c[0][1] / 3
        self.FalseNeg = d[0][1]
        d[1][0] = c[1][0] / 3
        self.FalsePos = d[1][0]
        d[0][0] = c[0][0] / 3
        self.TruePos = d[0][0]
        self.normalize = d
        return d

    @staticmethod
    def __normalize_rearrange_matrix(c):
        d = numpy.zeros((2, 2))
        d[1][1] = c[0][0]
        d[0][1] = c[1][0]
        d[1][0] = c[0][1]
        d[0][0] = c[1][1]
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
