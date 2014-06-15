# /usr/bin/env python
# -*- coding:utf-8 -*-

class Evaluator(object):
    '''Evaluate class'''

    def eval(self, s):
        '''Evaluate string'''
        if len(s) == 0:
            raise Exception

        if '+' in s:
            parts = s.split('+')
            return int(parts[0]) + int(parts[1])
        elif '-' in s:
            parts = s.split('-')
            return int(parts[0]) - int(parts[1])
        else:
            return int(s)
