# /usr/bin/env python
# -*- coding:utf-8 -*-

import nose.tools as assrt
from evaluator import *

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

    def test_AddingTwoNumbers(self):
        self.checkEvaluation("1+2", 3)

    def test_SubtractingTwoNumbers(self):
        self.checkEvaluation("88-20", 68)

class TestOperand(object):
    def test_ConstructorSetsValuePropertyCorrectly(self):
        sut = Operand("123")
        assrt.eq_(123, sut.value)

class TestParser(object):
    def test_ParseReturnsAdditionElements(self):
        sut = Parser()
        result = list(sut.parse("1+2"))
        assrt.eq_(len(result), 3)
        assrt.ok_(isinstance(result[0], Operand))
        assrt.ok_(isinstance(result[1], Operator))
        assrt.ok_(isinstance(result[2], Operand))

class TestOperatorFactory(object):
    def test_PlusSignReturnsAddOperator(self):
        sut = OperatorFactory()
        result = sut.create('+')
        assrt.ok_(isinstance(result, AddOperator))

    def test_MinusSignReturnsSubOperator(self):
        sut = OperatorFactory()
        result = sut.create('-')
        assrt.ok_(isinstance(result, SubOperator))

    @assrt.raises(Exception)
    def test_UnknownSignThrowsException(self):
        sut = OperatorFactory()
        sut.create('x')

class TestAddOperator(object):
    def test_AddOperatorComputesCorrectValue(self):
        sut = AddOperator()
        result = sut.compute(Operand("10"), Operand("20"))
        assrt.eq_(result, 30)

class TestSubOperator(object):
    def test_SubtractionOperatorComputesCorrectValue(self):
        sut = SubOperator()
        result = sut.compute(Operand("20"), Operand("10"))
        assrt.eq_(result, 10)
