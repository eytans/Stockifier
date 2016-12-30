from Classifiers import *
from Utilities import *
from unittest import TestCase


class TestConnectionStrengthClassifier(TestCase):
    def setUp(self):
        self.data, self.classes = ready_training_data('ABC', history_range=1)
        self.ld = LearningData()
        markets = [clean_market_name(m) for m in self.ld.get_market_names()]
        cols = self.data.columns
        self.market_fields = {m: [c for c in cols if m in str(c)] for m in markets}
        self.clf = classifiers.ConnectionStrengthClassifier()
        self.relations = [0.5]*len(markets)
        self.cols = list(self.market_fields.values())
        self.cols = [c for c in self.cols if len(c) > 0]

    def test_fit(self):
        self.assertIsNotNone(self.clf.fit(self.data, self.classes, self.cols, self.relations))

    def test_predict(self):
        self.fail()

    def test_predict_proba(self):
        self.fail()
