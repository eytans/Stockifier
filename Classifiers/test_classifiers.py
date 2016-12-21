from Classifiers.classifiers import create_quarter_clusterer
from Utilities.orginizers import LearningData
from unittest import TestCase
import logging


class TestCreate_quarter_clusterer(TestCase):
    def test_create_quarter_clusterer(self):
        logging.getLogger().setLevel(logging.DEBUG)
        clusterer = create_quarter_clusterer(LearningData())
        self.assertIsNotNone(clusterer)
