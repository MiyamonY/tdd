# /usr/bin/env python
# -*- coding:utf-8 -*-

from evaluator import Evaluator
import nose.tools as assrt

class TestAcceptance(object):
    
    def test_CanAddTwoIntegerNumbers(self):
        sut = Evaluator()
        result = sut.eval("10 + 25")
        assrt.eq_(result, 35)

    def test_CanSubtractTwoIntegerNumbers(self):
        sut = Evaluator()
        result = sut.eval("300 -5")
        assrt.eq_(result, 295)
