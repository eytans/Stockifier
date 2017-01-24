import pandas
from sklearn.metrics import confusion_matrix
import numpy
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


class ConfusionMatrix(object):
    def __init__(self, stock, model,strength=None,connections=None):
        print("26")
        # ready train data
        d, c = stock
        self.data, self.classes = stock

        #extract trues and falses
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
        # self.target_names = ["Predict True","Predict False"]

    def __repr__(self):
        st = ""
        st+=str(self.models)
        st+=("\nAccuracy: "+str(self.accuracy))
        return st

    def __str__(self):
        return self.__repr__()

    def calc_mat(self):
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
        self.normalize_matrix()
        self.accuracy = 100 * (self.TrueNeg * 0.8 + self.TruePos * 0.2)
        return self.normalize

    def normalize_matrix(self):
        d = numpy.zeros((2, 2))
        c = self.cnf_matrix
        d[1][1] = c[0][0] / (c[1][0] + c[0][0])
        self.TrueNeg = d[1][1]
        d[0][1] = c[1][0] / (c[1][0] + c[0][0])
        self.FalseNeg = d[0][1]
        d[1][0] = c[0][1] / (c[1][1] + c[0][1])
        self.FalsePos = d[1][0]
        d[0][0] = c[1][1] / (c[1][1] + c[0][1])
        self.TruePos = d[0][0]
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
