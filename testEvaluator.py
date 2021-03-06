# /usr/bin/env python
# -*- coding:utf-8 -*-

import nose.tools as assrt
import mock
from evaluator import *

def eq_(result, expected, precision=0.001):
    assrt.ok_(expected - precision <= result <= expected + precision)

class TestEvaluator(object):
    '''tests for Evaluator class'''
    
    def create_parser(self):
        return Parser(OperatorFactory(), OperandFactory())

    @assrt.raises(Exception)
    def test_NullOrEmpytStringThrowsException(self):
        '''calling with empty string, throws eception'''
        parser = self.create_parser()
        sut = Evaluator(parser)
        sut.eval("")

    def checkEvaluation(self, s, expected, precision = 0.0001):
        parser = self.create_parser()
        sut = Evaluator(parser)
        eq_(sut.eval(s), expected, precision)

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

    def test_MultiplyingTwoNumbers(self):
        self.checkEvaluation("12*3", 36)

    def test_DividingTwoNumbers(self):
        self.checkEvaluation("12/3", 4)

    def test_TwoOperations(self):
        self.checkEvaluation("2*3-5", 1)

    def test_TwoOperationsRespectingPrecedence(self):
        self.checkEvaluation("2+3*5", 17)

    def test_NegativeNumber(self):
        self.checkEvaluation("-3", -3)

    def test_NumberInParentheses(self):
        self.checkEvaluation("(3)", 3)

    def test_NegativeNumberInParentheses(self):
        self.checkEvaluation("(-3)", -3)

    def test_AddNegativeNumberInParenetheses(self):
        self.checkEvaluation("2+(-3)", -1)

    def test_FloatingPointNumber(self):
        self.checkEvaluation("1.5", 1.5, 0.01)

class TestElementList(object):
    def test_FindOperationReturnsFirstOperation(self):
        loperand = Operand(0)
        op = AddOperator()
        roperand = Operand(0)
        sut = ElementList([Operand(0), Operand(0),
                           loperand, op, roperand])
        result = sut.find_operation()
        assrt.eq_(loperand, result.loperand)
        assrt.eq_(op, result.op)
        assrt.eq_(roperand, result.roperand)

    def test_RelaceOperationWorks(self):
        loperand = Operand(0)
        op = AddOperator()
        roperand = Operand(0)
        sut = ElementList([loperand, op, roperand])
        operation = Operation(loperand, op, roperand)
        sut.replace_operation(operation, Operand(0))
        result = sut.find_operation()
        assrt.eq_(result, None)

    def test_ReplaceOperationReplaceTheCorrectOne(self):
        other_opd1 = Operand(0)
        other_op = AddOperator()
        other_opd2 = Operand(0)
        loperand = Operand(0)
        op = AddOperator()
        roperand = Operand(0)
        sut = ElementList([other_opd1, other_op, other_opd2,
                           loperand, op, roperand])
        operation = Operation(loperand, op, roperand)
        sut.replace_operation(operation, Operand(0))
        result = sut.find_operation()
        assrt.eq_(other_opd1, result.loperand)
        assrt.eq_(other_op, result.op)
        assrt.eq_(other_opd2, result.roperand)

    def test_FirstReturnsFirstElement(self):
        loperand = Operand(0)
        op = AddOperator()
        roperand = Operand(0)
        sut = ElementList([loperand, op, roperand])
        result = sut.first
        assrt.eq_(result, loperand)

    def test_FindOperationReturnsHighestPrecedence(self):
        loperand = Operand(0)
        op = MulOperator()
        roperand = Operand(0)
        sut = ElementList([Operand(0), AddOperator(),
                           Operand(0), loperand, op, roperand])
        result = sut.find_operation()
        assrt.eq_(result.loperand, loperand)
        assrt.eq_(result.op, op)
        assrt.eq_(result.roperand, roperand)

    def test_FindOperationCanHandleNegativeNumbers(self):
        op = SubOperator()
        roperand = Operand(1)
        sut = ElementList([op, roperand])
        result = sut.find_operation()
        assrt.eq_(result.loperand.value, 0)
        assrt.eq_(result.op, op)
        assrt.eq_(result.roperand, roperand)
        
    def test_FindOperatationCanHandleTwoSuccessiveOperators(self):
        opd1 = Operand(1)
        op1  = AddOperator()
        op2  = SubOperator(10)
        opd2 = Operand(2)
        sut  = ElementList([opd1, op1, op2, opd2])
        result = sut.find_operation()
        assrt.eq_(result.loperand.value, 0)
        assrt.eq_(result.op, op2)
        assrt.eq_(result.roperand, opd2)

class TestOprandFactory(object):
    def get_operand(self, value):
        sut = OperandFactory()
        return sut.create(value)

    def test_CreateReturnsOperand(self):
        result = self.get_operand(5)
        assrt.ok_(isinstance(result, Operand))

    def test_CreateReturnsOperandWithCorrectValue(self):
        result = self.get_operand(10)
        eq_(result.value, 10)

    def test_CreateReturnsOperandWithCorrectFloatingPoint(self):
        result = self.get_operand(5.73)
        eq_(result.value, 5.73, 0.01)

    def test_ReplaceOperationCanHandleNegativeNumbers(self):
        op = SubOperator()
        roperand = Operand(1)
        sut = ElementList([op, roperand])
        operation = sut.find_operation()
        sut.replace_operation(operation, Operand(-1))
        assrt.eq_(sut.first.value, -1)
        assrt.eq_(sut.find_operation(), None)

class TestOperand(object):
    def test_ConstructorSetsValuePropertyCorrectly(self):
        sut = Operand(123)
        eq_(sut.value, 123)

class TestParser(object):
    def parse(self, s):
        sut = Parser(OperatorFactory(), OperandFactory())
        return list(sut.parse(s))
        
    def test_ParseReturnsAdditionElements(self):
        result = self.parse(("1+2"))
        assrt.eq_(len(result), 3)
        assrt.ok_(isinstance(result[0], Operand))
        assrt.ok_(isinstance(result[1], Operator))
        assrt.ok_(isinstance(result[2], Operand))

    def test_ParserCallsOperandFactoryCreate(self):
        operand_factory = mock.Mock()
        operand_factory.create.return_value = None # don't care return value
        sut = Parser(OperatorFactory(), operand_factory)
        list(sut.parse("1"))    # yield doesn't return value, untill it is used
        assrt.eq_(operand_factory.create.call_count, 1)

    def test_MultipleOperandAndOperatorsAreParsedCorrectly(self):
        result = self.parse("1+2*3-4")
        assrt.eq_(len(result), 7)
        assrt.ok_(isinstance(result[0], Operand))
        assrt.ok_(isinstance(result[1], Operator))
        assrt.ok_(isinstance(result[2], Operand))
        assrt.ok_(isinstance(result[3], Operator))
        assrt.ok_(isinstance(result[4], Operand))
        assrt.ok_(isinstance(result[5], Operator))

    def test_FloatingPointNumber(self):
        result = self.parse("1.5")
        assrt.eq_(len(result), 1)
        eq_(result[0].value, 1.5, 0.01)

    def test_NegativeNumber(self):
        result = self.parse("-3")
        assrt.eq_(len(result), 2)
        assrt.ok_(isinstance(result[0], SubOperator))
        assrt.eq_(result[1].value, 3)

    def test_NumberInParentheses(self):
        result = self.parse("(3)")
        assrt.eq_(len(result), 1)
        assrt.eq_(result[0].value, 3)

    def test_OperatorsInParenthesesGetAPrecedenceBoost(self):
        result = self.parse("(1+2)")
        assrt.eq_(len(result), 3)
        assrt.eq_(result[0].value, 1)
        assrt.eq_(result[1].precedence, 11)
        assrt.eq_(result[2].value, 2)

    @assrt.raises(Exception)
    def test_TooManyOpenParentheses(self):
        self.parse("(1")

    @assrt.raises(Exception)
    def test_TooManyCloseParentheses(self):
        self.parse("1)")

    @assrt.raises(ValueError)
    def test_DoubleDecimalPoint(self):
        self.parse("1.5.7")

    def test_ExpressioWithSpaces(self):
        result = self.parse("1 + 2")
        assrt.eq_(len(result), 3)

    def test_SymbolExpression(self):
        sut = Parser(OperatorFactory(), OperandFactory(), {"x": 10})
        result = list(sut.parse("x"))
        assrt.eq_(len(result), 1)
        assrt.eq_(result[0].value, 10)

class TestOperatorFactory(object):
    def setUp(self):
        self.sut = OperatorFactory()

    def check(self, op, ty):
        result = self.sut.create(op, 0)
        assrt.ok_(isinstance(result, ty))

    def test_PlusSignReturnsAddOperator(self):
        self.check('+', AddOperator)

    def test_MinusSignReturnsSubOperator(self):
        self.check('-', SubOperator)

    def test_MulSignReturnsMulOperator(self):
        self.check('*', MulOperator)

    def test_DivSignReturnsDivOperator(self):
        self.check('/', DivOperator)

    @assrt.raises(Exception)
    def test_UnknownSignThrowsException(self):
        sut = OperatorFactory()
        sut.create('x', 0)

class TestOperator(object):
    def test_OperatorPrecedenceIsSetCorrect(self):
        assrt.eq_(AddOperator().precedence, 1)
        assrt.eq_(SubOperator().precedence, 1)
        assrt.eq_(MulOperator().precedence, 2)
        assrt.eq_(DivOperator().precedence, 2)

class TestAddOperator(object):
    def test_AddOperatorComputesCorrectValue(self):
        sut = AddOperator()
        result = sut.compute(Operand(10), Operand(20))
        eq_(result, 30)

    def test_TakesPrecedenceBoostIntoAccount(self):
        sut = AddOperator(7)
        assrt.eq_(sut.precedence, 8)
        
class TestSubOperator(object):
    def test_SubtractionOperatorComputesCorrectValue(self):
        sut = SubOperator()
        result = sut.compute(Operand(20), Operand(10))
        eq_(result, 10)

    def test_TakesPrecedenceBoostIntoAccount(self):
        sut = SubOperator(7)
        assrt.eq_(sut.precedence, 8)

class TestMulOperator(object):
    def test_MulOperatorComputesCorrectValue(self):
        sut = MulOperator()
        result = sut.compute(Operand(10), Operand(25))
        eq_(result, 250)

    def test_TakesPrecedenceBoostIntoAccount(self):
        sut = MulOperator(7)
        assrt.eq_(sut.precedence, 9)

class TestDivOperator(object):
    def test_DivOperatorComputesCorrectValue(self):
        sut = DivOperator()
        result = sut.compute(Operand(20), Operand(10))
        eq_(result, 2)

    def test_TakesPrecedenceBoostIntoAccount(self):
        sut = DivOperator(7)
        assrt.eq_(sut.precedence, 9)
