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

        parser = Parser()
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
    def parse(self, s):
        '''parse string'''
        operator_factory = OperatorFactory()
        operand = ""
        for curr_char in s:
            if curr_char.isdigit():
                operand += curr_char
            else:
                yield Operand(operand)
                operand = ""
                yield operator_factory.create(curr_char)

        if operand != "":
            yield Operand(operand)

class Element(object):
    '''Operand, Operator's base class(using dynamic typing language,
    this class is useless)'''
    pass

class Operand(Element):
    '''operand class'''
    def __init__(self, s):
        self.value = int(s)

class Operator(Element):
    '''operator class'''
    __metaclass__ = abc.ABCMeta

    def __init__(self, c):
        self._value = c

    @abc.abstractmethod
    def compute(self, left, right):
        raise NotImplementedError()

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

