from Utilities.orginizers import *
from unittest import TestCase
from Classifiers import classifiers


class TestTrainingData(TestCase):
    def setUp(self):
        self.ld = LearningData()
        self.td = TrainingData('ISIS')

    def test_add_history_fields_are_not_nan(self):
        self.td.add_history(10)
        column_count = len(self.td.data.columns)
        data, classes = self.td.get()
        self.assertIsNotNone(data)
        self.assertIsNotNone(classes)
        self.assertGreater(len(data.columns), column_count*0.9)
        self.assertEquals(0, sum(classes.isnull()))
        for c in data.columns:
            self.assertEquals(0, sum(data[c].isnull()))
        self.assertGreater(data.shape[0], 1000)

    def test_transform(self):
        data = self.td.transform(self.ld.get_stock_data('ISIS'))
        self.assertIsNotNone(data)
        self.assertGreaterEqual(data.shape[0], 1000)

    def test_get(self):
        data, classes = self.td.get()
        self.assertIsNotNone(data)
        self.assertIsNotNone(classes)
        self.assertGreater(data.shape[0], 1000)
        self.assertEquals(data.shape[0], classes.shape[0])

    def test_quarterizer_cut_by_clust(self):
        from sklearn.cluster import KMeans
        data, classes = self.td.get()
        clusters = 6
        quarterizer = classifiers.Quarterizer().fit(data)
        quarters = quarterizer.transform(data)
        q_clf = KMeans(n_clusters=clusters).fit(quarters.drop(['start', 'end'], axis=1))
        quarters_c = q_clf.predict(quarters.drop(['start', 'end'], axis=1))
        clust_to_data = quarterizer.cut_by_classes(data, quarters, quarters_c)
        self.assertIsInstance(clust_to_data, dict)
        self.assertGreater(len(clust_to_data), 0)
