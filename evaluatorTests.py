# /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from evaluator import Evaluator

class EvaluatorTests(unittest.TestCase):
    '''tests for Evaluator class'''

    def test_NullOrEmpytStringThrowsException(self):
        '''calling with empty string, throws eception'''
        sut = Evaluator()
        self.assertRaises(Exception, sut.eval, "")

if __name__ == '__main__':
    unittest.main()
