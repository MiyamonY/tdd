# /usr/bin/env python
# -*- coding:utf-8 -*-

from evaluator import Evaluator
import nose.tools as assrt

class TestAcceptance(object):

    def checkEvaluation(self, s, expected):
        sut = Evaluator()
        result = sut.eval(s)
        assrt.eq_(result, expected)
        
    def test_CanAddTwoIntegerNumbers(self):
        self.checkEvaluation("10+25", 35)

    def test_CanSubtractTwoIntegerNumbers(self):
        self.checkEvaluation("300-5", 295)

    def test_CanMultiplyTwoIntegerNumbers(self):
        self.checkEvaluation("12*30", 360)

    def test_CanDivideTwoIntegerNumbers(self):
        self.checkEvaluation("30/5", 6)
