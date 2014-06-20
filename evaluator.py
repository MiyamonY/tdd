# /usr/bin/env python
# -*- coding:utf-8 -*-

'''
Evaluate expression
'''
import abc

class Evaluator(object):
    '''Evaluate class'''

    def __init__(self, parser):
        self.parser = parser

    def eval(self, s):
        '''Evaluate string'''
        if len(s) == 0:
            raise Exception

        elements = ElementList(list(self.parser.parse(s)))
        operation = elements.find_operation()

        while operation != None:
            new_element = operation.compute()
            elements.replace_operation(operation, new_element)
            operation = elements.find_operation()

        return elements.first.value

class Parser(object):
    ''' Parser class'''
    def __init__(self, operator_factory, operand_factory):
        self.operator_factory = operator_factory
        self.operand_factory = operand_factory

    def parse(self, s):
        '''parse string'''
        operand = ""
        for curr_char in s:
            if curr_char.isdigit() or curr_char == '.':
                operand += curr_char
            else:
                yield self.operand_factory.create(float(operand))
                operand = ""
                yield self.operator_factory.create(curr_char)

        if operand != "":
            yield self.operand_factory.create(float(operand))

class Element(object):
    '''Operand, Operator's base class(using dynamic typing language,
    this class is useless)'''
    pass

class ElementList(object):
    def __init__(self, elements):
        self.elements = elements

    def find_operation(self):
        operators = [x for x in self.elements if isinstance(x, Operator)]

        if operators == []: return None

        max_precedence = max([x.precedence for x in operators])

        first_op = [x for x in operators
                    if x.precedence == max_precedence][0]

        index = self.elements.index(first_op)

        return Operation(self.elements[index-1],
                         self.elements[index],
                         self.elements[index+1])

    def replace_operation(self, operation, operand):
        index = self.elements.index(operation.loperand)
        del self.elements[index+2]
        del self.elements[index+1]
        self.elements[index] = operand

    def __getattr__(self, name):
        if name == 'first':
            return self.elements[0]
        else:
            raise AttributeError()

class IOperandFactory(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self, value):
        raise NotImplementedError()

class OperandFactory(IOperandFactory):
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
        self.precedence = 0

    @abc.abstractmethod
    def compute(self, left, right):
        raise NotImplementedError()

class AddOperator(Operator):
    def __init__(self):
        super(AddOperator, self).__init__('+')
        self.precedence = 1

    def compute(self, left, right):
        '''compute given value by add'''
        return left.value + right.value

class SubOperator(Operator):
    def __init__(self):
        super(SubOperator, self).__init__('-')
        self.precedence = 1

    def compute(self, left, right):
        '''compute given value by sub'''
        return left.value - right.value

class MulOperator(Operator):
    def __init__(self):
        super(MulOperator, self).__init__('*')
        self.precedence = 2

    def compute(self, left, right):
        '''comptue given value by multi'''
        return left.value * right.value

class DivOperator(Operator):
    def __init__(self):
        super(DivOperator, self).__init__('/')
        self.precedence = 2

    def compute(self, left, right):
        return left.value / right.value

class Operation(object):
    def __init__(self, loperand, op, roperand):
        self.loperand = loperand
        self.op = op
        self.roperand = roperand

    def compute(self):
        return Operand(self.op.compute(self.loperand, self.roperand))
