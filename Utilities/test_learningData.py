import traceback
from Utilities.orginizers import LearningData
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
