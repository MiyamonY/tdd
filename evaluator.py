# /usr/bin/env python
# -*- coding:utf-8 -*-

class Evaluator(object):
    '''Evaluate class'''

    def eval(self, s):
        '''Evaluate string'''
        if len(s) == 0:
            raise Exception

        parser = Parser()
        elements = list(parser.parse(s))

        if len(elements) == 3:
            if elements[1].value == '+':
                return int(elements[0].value) + int(elements[2].value)

            if elements[1].value == '-':
                return int(elements[0].value) - int(elements[2].value)
        else:
            return int(s)

class Parser(object):
    def parse(self, s):
        operand = ""
        for curr_char in s:
            if curr_char.isdigit():
                operand += curr_char
            else:
                yield Operand(operand)
                operand = ""
                yield Operator(curr_char)

        if not operand == "":
            yield Operand(operand)

class Element(object):
    pass

class Operand(Element):
    def __init__(self, s):
        self.value = s

class Operator(Element):
    def __init__(self, c):
        self.value = c
