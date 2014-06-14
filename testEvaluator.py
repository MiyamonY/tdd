# /usr/bin/env python
# -*- coding:utf-8 -*-

import nose.tools as assrt
from evaluator import Evaluator

class TestEvaluator(object):
    '''tests for Evaluator class'''

    @assrt.raises(Exception)
    def test_NullOrEmpytStringThrowsException(self):
        '''calling with empty string, throws eception'''
        sut = Evaluator()
        sut.eval("")

