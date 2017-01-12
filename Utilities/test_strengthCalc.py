from unittest import TestCase
from Utilities import orginizers, clustering
import logging
import timeit

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

    def test_get_strength_stock(self):
        d = self.strength.get_strength_stock(stock='DEPO',  min_number=5, max_number=20, step=5,
                                       threshold=0.5)
        self.assertEqual(len(d.keys()),20)
        self.assertEqual(set(d.keys()), set(self.ld.get_market_names()))
        for k in d.keys():
            self.assertGreaterEqual(d[k], 0.0)
            self.assertLessEqual(d[k], 1.0)


class TestStrengthCalcTimes(TestCase):
    @classmethod
    def setUpClass(cls):
        logging.getLogger().setLevel(logging.INFO)

    def setUp(self):
        self.runs = 3
        self.expected_init_time = 25
        self.expected_array_time = 21
        self.expected_ready_stock_time = 0.001
        self.expected_strength_calc = 0.5

    def test_init_data_not_slow(self):
        t = timeit.timeit("clustering.StrengthCalc()", setup='from Utilities import clustering', number=self.runs)
        logging.info(t)
        self.assertGreaterEqual(self.expected_init_time, t)

    def test_create_array_of_clusters(self):
        setup = """
from Utilities import clustering
strength = clustering.StrengthCalc()
        """
        cmd = 'strength.create_array_of_clusters(min_number=1, max_number=100, step=1)'
        t = timeit.timeit(cmd, setup=setup, number=self.runs)/self.runs
        logging.info(t)
        self.assertGreaterEqual(self.expected_array_time, t)

    def test_ready_stock_to_predict(self):
        setup = """
from Utilities import clustering
strength = clustering.StrengthCalc()
        """
        cmd = "strength.ready_stock_to_predict(['ABC'])"
        t = timeit.timeit(cmd, setup=setup, number=self.runs)/self.runs
        logging.info(t)
        self.assertGreaterEqual(self.expected_ready_stock_time, t)

    def test_strength_calc(self):
        setup = """
from Utilities import clustering
strength = clustering.StrengthCalc()
market = clustering.market_stock_dic['Accident & Health Insurance (Financial)']
arr_clr = strength.create_array_of_clusters(min_number=1, max_number=100, step=1)
arr_clr.reverse()
stock_data = strength.ready_stock_to_predict(['ABC'])
market_data = strength.ready_stock_to_predict(market)
        """
        cmd = "strength._calc_strength(stock_data, market_data, arr_clr, 0.5)"
        t = timeit.timeit(cmd, setup=setup, number=self.runs)/self.runs
        logging.info(t)
        self.assertGreaterEqual(self.expected_strength_calc, t)

    def test_investigate_fail(self):
        from Utilities import clustering
        strength = clustering.StrengthCalc()
        dic = strength.get_strength_stock(stock='KRO',min_number=5,max_number=325,step=2,threshold=0.1)
        for item in dic.items():
            self.assertGreaterEqual(item[1],0)




