from unittest import TestCase
from Utilities import orginizers,clustering

class TestStrengthCalc(TestCase):
    def setUp(self):
        self.ld = orginizers.LearningData()
        self.strength = clustering.StrengthCalc()

    def test_create_clustering_obj(self):
        clr3 = self.strength.create_clustering_obj(3)
        print(clr3.labels_)

    def test_create_array_of_clusters(self):
        arr_clr = self.strength.create_array_of_clusters(5,20,5)
        for c in arr_clr:
            self.assertIn(0,c.labels_)

    def test_get_strength_has_legal_result(self):
        d = self.strength.get_strength(stock='ABC', market='Accident & Health Insurance (Financial)', min_number=5, max_number=100, step=5,
                                       threshold=0.5)
        self.assertGreaterEqual(d, 0.0)
        self.assertLessEqual(d, 1.0)

    def test_get_strength_has_non_trivial_result(self):
        for st in self.strength.stocks:
            d = self.strength.get_strength(stock=st, market='Accident & Health Insurance (Financial)', min_number=5,
                                           max_number=100, step=5, threshold=0.6)
            if d > 0.0:
                return
        self.fail("Couldn't find a stock with matching of over %75 to market")


