"""Project4 Test Cases
CPE202

Darya Darvish
"""

import unittest
from SearchEngine import HashTableLinear, HashTableQuadratic, HashTableSepchain, import_stopwords, SearchEngine


class SearchEngineTestCase(unittest.TestCase):
    def test_Search_1(self):
        s = SearchEngine("docs", import_stopwords("stop_words.txt", HashTableLinear()))
        query1 = s.parse_words(["ADT"])
        query2 = s.parse_words(["Computer Science"])
        self.assertEqual(s.search(query1), [('docs/data_structure.txt', 0.017277012046530055)])
        self.assertEqual(s.search(query2), [('docs/test.txt', 1.0),
                                            ('docs/information_retrieval.txt', 0.017241379310344827),
                                            ('docs/hash_table.txt', 0.009523809523809525)])

    def test_Search_2(self):
        s = SearchEngine("docs", import_stopwords("stop_words.txt", HashTableQuadratic()))
        query1 = s.parse_words(["ADT"])
        query2 = s.parse_words(["Computer Science"])
        self.assertEqual(s.search(query1), [('docs/data_structure.txt', 0.017277012046530055)])
        self.assertEqual(s.search(query2), [('docs/test.txt', 1.0),
                                            ('docs/information_retrieval.txt', 0.017241379310344827),
                                            ('docs/hash_table.txt', 0.009523809523809525)])

    def test_Search_3(self):
        s = SearchEngine("docs", import_stopwords("stop_words.txt", HashTableSepchain()))
        query1 = s.parse_words(["ADT"])
        query2 = s.parse_words(["Computer Science"])
        self.assertEqual(s.search(query1), [('docs/data_structure.txt', 0.017277012046530055)])
        self.assertEqual(s.search(query2), [('docs/test.txt', 1.0),
                                            ('docs/information_retrieval.txt', 0.017241379310344827),
                                            ('docs/hash_table.txt', 0.009523809523809525)])


def main():
    # execute unit tests
    unittest.main()


if __name__ == '__main__':
    # execute main() function
    main()
