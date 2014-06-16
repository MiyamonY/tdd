# /usr/bin/env python
# -*- coding:utf-8 -*-

'''
Evaluate expression
'''
import abc

class Evaluator(object):
    '''Evaluate class'''

    def eval(self, s):
        '''Evaluate string'''
        if len(s) == 0:
            raise Exception

        parser = Parser(OperatorFactory(), OperandFactory())
        elements = list(parser.parse(s))

        if len(elements) == 3:
            left = elements[0]
            op = elements[1]
            right = elements[2]
            return op.compute(left, right)
        else:
            return int(s)

class Parser(object):
    ''' Parser class'''
    def __init__(self, operator_factory, operand_factory):
        self.operator_factory = operator_factory
        self.operand_factory = operand_factory

    def parse(self, s):
        '''parse string'''
        operand = ""
        for curr_char in s:
            if curr_char.isdigit():
                operand += curr_char
            else:
                yield Operand(int(operand))
                operand = ""
                yield self.operator_factory.create(curr_char)

        if operand != "":
            yield Operand(int(operand))

class Element(object):
    '''Operand, Operator's base class(using dynamic typing language,
    this class is useless)'''
    pass

class OperandFactory(object):
    def create(self, value):
        return Operand(value)

class Operand(Element):
    '''operand class'''
    def __init__(self, s):
        self.value = s

class OperatorFactory(object):
    def create(self, op):
        if op == '+':
            return AddOperator()
        elif op == '-':
            return SubOperator()
        elif op == '*':
            return MulOperator()
        elif op == '/':
            return DivOperator()
        else:
            raise Exception("Unknown operator [{0}]".format(op))

class Operator(Element):
    '''operator class'''
    __metaclass__ = abc.ABCMeta

    def __init__(self, c):
        self._value = c

    @abc.abstractmethod
    def compute(self, left, right):
        raise NotImplementedError()

class AddOperator(Operator):
    def __init__(self):
        super(AddOperator, self).__init__('+')

    def compute(self, left, right):
        '''compute given value by add'''
        return left.value + right.value

class SubOperator(Operator):
    def __init__(self):
        super(SubOperator, self).__init__('-')

    def compute(self, left, right):
        '''compute given value by sub'''
        return left.value - right.value

class MulOperator(Operator):
    def __init__(self):
        super(MulOperator, self).__init__('*')

    def compute(self, left, right):
        '''comptue given value by multi'''
        return left.value * right.value

class DivOperator(Operator):
    def __init__(self):
        super(DivOperator, self).__init__('/')

    def compute(self, left, right):
        return left.value / right.value

