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

        elements = list(self.parser.parse(s))
        
        while len(elements) > 1:
            tup = self.find_operation(elements)
            new_element = self.compute(tup[1])
            self.replace_operation(elements, tup[0], new_element)
        return elements[0].value

    def find_operation(self, elements): 
        for i, x in enumerate(elements):
            if isinstance(x, Operator):
                return (i - 1, Operation(elements[i - 1],
                                     elements[i],
                                     elements[i + 1]))
        return None

    def compute(self, op):
        return Operand(op.op.compute(op.loperand, op.roperand))

    def replace_operation(self, elements, index, operand):
        del elements[index + 2]
        del elements[index + 1]
        del elements[index]
        elements.insert(index, operand)

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
                yield self.operand_factory.create(int(operand))
                operand = ""
                yield self.operator_factory.create(curr_char)

        if operand != "":
            yield self.operand_factory.create(int(operand))

class Element(object):
    '''Operand, Operator's base class(using dynamic typing language,
    this class is useless)'''
    pass

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

class Operation(object):
    def __init__(self, loperand, op, roperand):
        self.loperand = loperand
        self.op = op
        self.roperand = roperand

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

