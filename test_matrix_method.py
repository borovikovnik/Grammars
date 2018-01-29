import unittest
import os
import glob
from matrix_method import matrix_method
from answers import answers_homsky
from utils import count_res


class TestMatrix(unittest.TestCase):
    def test_matrix_method(self):
        for graph in glob.glob("./data/*"):
            for grammar in glob.glob("./grammars/homsky/*"):
                res = count_res(matrix_method(grammar, graph, test=True))
                print(os.path.basename(graph), os.path.basename(grammar), res)
                self.assertEqual(res, answers_homsky[(os.path.basename(graph), os.path.basename(grammar))])


if __name__ == '__main__':
    unittest.main()
