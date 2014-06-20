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
    BOOST = 10
    def __init__(self, operator_factory, operand_factory, symbols=None):
        self.operator_factory = operator_factory
        self.operand_factory = operand_factory
        self.symbols = symbols

    def parse(self, s):
        '''parse string'''
        precedence_boost = 0

        operand = ""
        for curr_char in s:
            if curr_char.isspace(): continue

            if curr_char.isalnum() or curr_char == '.':
                operand += curr_char
            else:
                if operand != "":
                    yield self.operand_factory.create(self.get_operand(operand))

                operand = ""
                if curr_char == '(':
                    precedence_boost += Parser.BOOST
                elif curr_char == ')':
                    precedence_boost -= Parser.BOOST
                else:
                    yield \
                        self.operator_factory.create(curr_char, precedence_boost)

        if operand != "":
            yield self.operand_factory.create(self.get_operand(operand))

        if precedence_boost > 0:
            raise Exception("Too many open parentheses")

        if precedence_boost < 0:
            raise Exception("Too many close parentheses")

    def get_operand(self, operand):
        return self.symbols[operand] if operand[0].isalpha() else float(operand)

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

        return Operation(self.get_operand(index-1),
                         self.elements[index],
                         self.get_operand(index+1))

    def get_operand(self, index):
        return \
            self.elements[index] if 0 <= index < len(self.elements) \
            and isinstance(self.elements[index], Operand) else Operand(0)

    def replace_operation(self, operation, operand):
        index = self.elements.index(operation.op)
        if self.get_operand(index+1) == operation.roperand:
            del self.elements[index+1]
        self.elements[index] = operand
        if self.get_operand(index-1) == operation.loperand:
            del self.elements[index-1]

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
    def create(self, op, precedence_boost):
        if op == '+':
            return AddOperator(precedence_boost)
        elif op == '-':
            return SubOperator(precedence_boost)
        elif op == '*':
            return MulOperator(precedence_boost)
        elif op == '/':
            return DivOperator(precedence_boost)
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
    def __init__(self, precedence_boost = 0):
        super(AddOperator, self).__init__('+')
        self.precedence = 1 + precedence_boost

    def compute(self, left, right):
        '''compute given value by add'''
        return left.value + right.value

class SubOperator(Operator):
    def __init__(self, precedence_boost = 0):
        super(SubOperator, self).__init__('-')
        self.precedence = 1 + precedence_boost

    def compute(self, left, right):
        '''compute given value by sub'''
        return left.value - right.value

class MulOperator(Operator):
    def __init__(self, precedence_boost = 0):
        super(MulOperator, self).__init__('*')
        self.precedence = 2 + precedence_boost

    def compute(self, left, right):
        '''comptue given value by multi'''
        return left.value * right.value

class DivOperator(Operator):
    def __init__(self, precedence_boost = 0):
        super(DivOperator, self).__init__('/')
        self.precedence = 2 + precedence_boost

    def compute(self, left, right):
        return left.value / right.value

class Operation(object):
    def __init__(self, loperand, op, roperand):
        self.loperand = loperand
        self.op = op
        self.roperand = roperand

    def compute(self):
        return Operand(self.op.compute(self.loperand, self.roperand))
