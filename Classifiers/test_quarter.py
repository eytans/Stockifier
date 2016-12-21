from Utilities.orginizers import LearningData
from Classifiers import classifiers
from unittest import TestCase


class TestQuarter(TestCase):
    def setUp(self):
        self.ld = LearningData()
        self.abc = self.ld.get_stock_data('ABC')
        cols = list(self.abc.columns)
        cols.remove('volume')
        cols.remove('open')
        self.abc = self.abc.drop(cols, axis=1)
        self.quarterer = classifiers.Quarter('ABC', self.abc)

    def test_interpolate_extra_points(self):
        self.assertIsNotNone(self.quarterer.interpolate_extra_points(360))
