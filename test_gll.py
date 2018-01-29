import unittest
import os
import glob
from gll import gll_method
from answers import answers_automata
from utils import count_res


class TestGLL(unittest.TestCase):
    def test_gll_method(self):
        for graph in glob.glob("./data/*"):
            for grammar in glob.glob("./grammars/automata/*"):
                res = count_res(gll_method(grammar, graph, test=True))
                print(os.path.basename(graph), os.path.basename(grammar), res)
                self.assertEqual(res, answers_automata[(os.path.basename(graph), os.path.basename(grammar))])


if __name__ == '__main__':
    unittest.main()
