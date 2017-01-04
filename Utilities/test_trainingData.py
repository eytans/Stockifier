from Utilities.orginizers import *
from unittest import TestCase


class TestTrainingData(TestCase):
    def setUp(self):
        self.ld = LearningData()
        self.td = TrainingData('ISIS')

    def test_add_history_fields_are_not_nan(self):
        self.td.add_history_fields(10)
        column_count = len(self.td.data.columns)
        data, classes = self.td.get()
        self.assertIsNotNone(data)
        self.assertIsNotNone(classes)
        self.assertGreater(len(data.columns), column_count*0.9)
        self.assertEquals(0, sum(classes.isnull()))
        for c in data.columns:
            self.assertEquals(0, sum(data[c].isnull()))
        self.assertGreater(data.shape[0], 1000)

    def test_transform(self):
        data = self.td.transform(self.ld.get_stock_data('ISIS'))
        self.assertIsNotNone(data)
        self.assertGreaterEqual(data.shape[0], 1000)

    def test_get(self):
        data, classes = self.td.get()
        self.assertIsNotNone(data)
        self.assertIsNotNone(classes)
        self.assertGreater(data.shape[0], 1000)
        self.assertEquals(data.shape[0], classes.shape[0])
