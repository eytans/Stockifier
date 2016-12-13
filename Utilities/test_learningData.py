import traceback
from Utilities.data_orginizers import LearningData
from unittest import TestCase


class TestLearningData(TestCase):
    def setUp(self):
        self.ld = LearningData()

    def test_get_stock_data(self):
        try:
            df = self.ld.get_stock_data('ABC')
            self.assertIsNotNone(df)
            s = df.shape
            self.assertGreater(s[0], 100)
            self.assertGreater(s[1], 100)
        except:
            traceback.print_exc()
            self.fail()
