import csv
import enumifiers
import classifiers
from unittest import TestCase


class TestGet_general_classifier(TestCase):
    def setUp(self):
        reader = csv.reader(open('Samples/adult/Dataset.data', 'r', newline=''), delimiter=' ')
        self.data = [r for r in reader]
        self.results = [r[-1] for r in self.data]
        e = enumifiers.Enumifier()
        self.results = [e[r] for r in self.results]
        self.samples = [row[:-1] for row in self.data]
        self.samples = enumifiers.EnumeratedTable(self.samples)

    def test_general_classifier_with_enumifiers(self):
        self.assertIsNotNone(classifiers.get_general_classifier(self.samples.data, self.results))


class Test_StockData(TestCase):
    def setUp(self):
        reader = csv.reader(open('Samples/Accident & Health Insurance (Financial)/AFL.csv', 'r', newline=''), delimiter=',')
        self.data = [r for r in reader]
        self.results = [r[-1] for r in self.data]
        e = enumifiers.Enumifier()
        self.results = [e[r] for r in self.results]
        self.samples = [row[:-1] for row in self.data]
        self.samples = enumifiers.EnumeratedTable(self.samples)

    def test_stocks_classifier_with_enumifiers(self):
        clf = classifiers.get_general_classifier(self.samples.data, self.results)
        self.assertIsNotNone(clf)