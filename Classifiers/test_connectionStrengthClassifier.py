from Classifiers import *
from Utilities import *
from sklearn.model_selection import cross_val_predict
from unittest import TestCase


class TestConnectionStrengthClassifier(TestCase):
    def setUp(self):
        self.data, self.classes = TrainingData('ABC').add_history(1).get()
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
