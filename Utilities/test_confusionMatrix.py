from Utilities.orginizers import TrainingData
from sklearn.tree import DecisionTreeClassifier
from Utilities.confusion_matrix import ConfusionMatrix
import pandas
from unittest import TestCase


class TestConfusionMatrix(TestCase):
    def setUp(self):
        self.td = TrainingData('SHW').add_history(10).set_threshold(0.8)

    def test___init__(self):
        stock = self.td.get()
        model = DecisionTreeClassifier(min_samples_leaf=0.05, max_depth=30)
        cm = ConfusionMatrix(stock, model)
        self.assertFalse(pandas.isnull(cm.TrueNeg))
        self.assertFalse(pandas.isnull(cm.TruePos))
