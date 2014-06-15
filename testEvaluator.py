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

    def checkEvaluation(self, s, expected):
        sut = Evaluator()
        assrt.eq_(sut.eval(s), expected)

    def test_OneDigitNumberIsEvaluatedToItsIntegerValue(self):
        self.checkEvaluation("7", 7)

    def test_OneDigitNumberIsEvaluatedItsIntegerValue_SecondAttempt(self):
        self.checkEvaluation("5", 5)

    def test_MultipleDiditNumberIsEvaluatedToItsIntegerValue(self):
        self.checkEvaluation("324", 324)
