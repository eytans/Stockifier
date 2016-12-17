import traceback
from Utilities.data_orginizers import LearningData
from unittest import TestCase
import datetime


class TestLearningData(TestCase):
    def setUp(self):
        self.ld = LearningData()
        self.df = self.ld.get_stock_data('ABC')
        self.start = datetime.datetime(2000, 5, 5)
        self.end = datetime.datetime(2005, 5, 5)

    def test_get_stock_data(self):
        try:
            self.assertIsNotNone(self.df)
            s = self.df.shape
            self.assertGreater(s[0], 100)
        except:
            traceback.print_exc()
            self.fail()

    def test_add_history_fields_doesnt_fail(self):
        self.assertIsNotNone(self.df)
        self.df = self.ld.slice_by_date(self.df, self.start, self.end)
        res = self.ld.add_history_fields(self.df, 'ABC', 10)
        self.assertGreater(res.shape[1], self.df[1])
