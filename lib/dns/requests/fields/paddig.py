# -*- coding: utf-8 -*-
import random
from field import RequestField

class Padding(RequestField):
    RANDOM_STRING = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    name = 'padding'
    default = 0
    separate = 63
    def __str__(self):
        arr = [random.choice(self.RANDOM_STRING) for x in xrange(self.separate)]
        res = '.'.join([''.join(arr) for y in xrange(self.value)])
        res = res[:self.value]
        if res[-1:] == '.':
            res = res[:-1] + random.choice(self.RANDOM_STRING)
        return res
