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

    def test_OneDigitNumberIsEvaluatedToItsIntegerValue(self):
        sut = Evaluator()
        result = sut.eval("7")
        assrt.eq_(result, 7)

    def test_OneDigitNumberIsEvaluatedItsIntegerValue_SecondAttempt(self):
        sut = Evaluator()
        result = sut.eval("5")
        assrt.eq_(result, 5)

    def test_MultipleDiditNumberIsEvaluatedToItsIntegerValue(self):
        sut = Evaluator()
        result = sut.eval("324")
        assrt.eq_(result, 324)
