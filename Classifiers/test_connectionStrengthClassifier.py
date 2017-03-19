from Classifiers import *
from Utilities import *
from sklearn.model_selection import cross_val_predict
from unittest import TestCase
from Utilities.confusion_matrix import ConfusionMatrix


class TestConnectionStrengthClassifier(TestCase):
    def setUp(self):
        self.sname = 'ABC'
        self.data, self.classes = TrainingData(self.sname).add_history(1).get()
        self.ld = LearningData()
        markets = [clean_market_name(m) for m in self.ld.get_market_names()]
        cols = self.data.columns
        self.market_fields = {m: [c for c in cols if m in str(c)] for m in markets}
        self.clf = classifiers.ConnectionStrengthClassifier()
        self.relations = [0.5]*len(markets)
        self.cols = list(self.market_fields.values())
        self.cols = [c for c in self.cols if len(c) > 0]

    def _fit(self):
        return self.clf.fit(self.data, self.classes, self.cols, self.relations)

    def test_fit(self):
        self.assertIsNotNone(self._fit())

    def test_predict(self):
        self.assertGreaterEqual(
            sum(cross_val_predict(self.clf, self.data, self.classes, fit_params={'connection_columns': self.cols,
                                  'strengths': self.relations}))/3, 0.75)

    def test_ConfusionMatrix_on_clasifier(self):
        from Utilities.clustering import StrengthCalc
        from Utilities import clean_market_name
        import pandas

        stock_names = ('SHW', 'MNK', 'BIO', 'KYTH', 'KRO')
        logging.getLogger().setLevel(logging.ERROR)
        stocks = [TrainingData(sn, ld=self.ld).add_history(10).set_threshold(0.8).get() for sn in stock_names]
        best_cut = 22
        tree_stocks = [
            (pandas.get_dummies(data.apply(lambda s: pandas.qcut(s.rank(method='first'), best_cut))), classes) for
            data, classes in stocks]

        # d, c = TrainingData('ABC', ld=self.ld).add_history(10).set_threshold(0.8).get()
        # self.data, self.classes = (pandas.get_dummies(d.apply(lambda s: pandas.qcut(s.rank(method='first'), 22))), c)

        sc = StrengthCalc()
        stock_strengths = [sc.get_strength_stock(sn, 5, 325, 2, 0.1) for sn in stock_names]
        clf = ConnectionStrengthClassifier()

        # cols = self.data.columns

        # cur_cols = []
        # cur_strengths = []
        # for m in self.ld.get_market_names():
        #     cur_cols.append(list(filter(lambda c: clean_market_name(m) in c, cols)))
        #     cur_strengths.append(stock_strength[m])

        from Utilities import clean_market_name

        cols = []
        for d, c in tree_stocks:
            cols.extend(d.columns)
        all_cols = set(cols)

        strengths = []
        connections_cols = []
        for i, sn in enumerate(stock_names):
            cur_cols = []
            cur_strengths = []
            for m in self.ld.get_market_names():
                cur_cols.append(list(filter(lambda c: clean_market_name(m) in c, all_cols)))
                cur_strengths.append(stock_strengths[i][m])
            connections_cols.append(cur_cols)
            strengths.append(cur_strengths)

        def run_strength_model(model, stocks=stocks, strength=strengths, cols=connections_cols):
            scores = {sn: [] for sn in stock_names}
            for sn, (data, classes), st, cs in zip(stock_names, stocks, strength, cols):
                scores[sn] = ConfusionMatrix((data, classes), model, st, cs)
            return scores

        con_model = ConnectionStrengthClassifier()
        st_accuracies = run_strength_model(con_model, tree_stocks)

        self.assertIsNotNone(st_accuracies)