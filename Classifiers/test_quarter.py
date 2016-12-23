from Utilities.orginizers import LearningData
from Classifiers import classifiers
from unittest import TestCase


class TestQuarter(TestCase):
    def setUp(self):
        self.ld = LearningData()
        self.abc = self.create_q_data('ABC')
        self.quarter = classifiers.Quarter(self.abc)

    def create_q_data(self, name):
        q = self.ld.get_stock_data(name)
        cols = list(q.columns)
        cols.remove('volume')
        cols.remove('open')
        q = q.drop(cols, axis=1)
        return q

    def test_interpolate_extra_points(self):
        self.assertIsNotNone(self.quarter.interpolate_extra_points(360))

    def test___add__(self):
        amrs = self.create_q_data('AMRS')
        q = classifiers.Quarter(amrs)
        added = q + self.quarter
        q.ready_quarter_data(24 * 60)
        self.quarter.ready_quarter_data(24 * 60)
        self.assertEqual(added.data.iloc[0][0], q.data.iloc[0][0] + self.quarter.data.iloc[0][0])

    def test_add_add_works(self):
        amrs = self.create_q_data('AMRS')
        q1 = classifiers.Quarter(amrs)
        alog = self.create_q_data('ALOG')
        q2 = classifiers.Quarter(alog)
        self.assertIsNotNone((q1 + q2 + self.quarter))

    def test___sub__(self):
        self.fail()

    def test___truediv__(self):
        self.assertIsNotNone(self.quarter / 5)
