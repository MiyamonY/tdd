# /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from evaluator import Evaluator

class AcceptanceTests(unittest.TestCase):
    
    def test_CanAddTwoIntegerNumbers(self):
        sut = Evaluator()
        result = sut.eval("10 + 25")
        self.assertEqual(result, 35)

    def test_CanSubtractTwoIntegerNumbers(self):
        sut = Evaluator()
        result = sut.eval("300 -5")
        self.assertEqual(result, 295)


if __name__ == '__main__':
    unittest.main()
