import Utilities
from Utilities.orginizers import LearningData
from Classifiers import classifiers
from unittest import TestCase


class TestQuarterDistance(TestCase):
    def setUp(self):
        self.ld = LearningData()
        self.abc = self.ld.get_stock_data('ABC')
        cols = list(self.abc.columns)
        cols.remove('volume')
        cols.remove('open')
        self.abc = self.abc.drop(cols, axis=1)
        self.quarterer = classifiers.QuarterDistance(4)

    def test_interpolate_extra_points(self):
        self.assertIsNotNone(self.quarterer.interpolate_extra_points(self.abc))

    def test_dist_returns_num(self):
        not_empty = False
        for q1, q2 in Utilities.iterate_couples(classifiers.QuarterDistance.split_by_quarters(self.abc)):
            not_empty = True
            self.assertGreaterEqual(self.quarterer.dist(q1, q2), 0)
        self.assertTrue(not_empty)
