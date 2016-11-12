from unittest import TestCase
import enumifiers
import csv


class TestEnumeratedTable(TestCase):
    def setUp(self):
        reader = csv.reader(open('Samples/adult/Dataset.data', 'r', newline=''), delimiter=' ')
        self.data = [r for r in reader]

    def test_enumeration_doesnt_crash(self):
        results = [r[-1] for r in self.data]
        e = enumifiers.Enumifier()
        results = [e[r] for r in results]
        self.assertTrue(results[0] is not None)

    def test_enumeration_table_doesnt_crash(self):
        e = enumifiers.EnumeratedTable(self.data)
        self.assertTrue(e[0][0] is not None)