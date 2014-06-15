# /usr/bin/env python
# -*- coding:utf-8 -*-

class Evaluator(object):
    '''Evaluate class'''

    def eval(self, s):
        '''Evaluate string'''
        if len(s) == 0:
            raise Exception
        else:
            return int(s)
