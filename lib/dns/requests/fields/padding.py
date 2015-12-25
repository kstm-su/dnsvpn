# -*- coding: utf-8 -*-
from field import RequestField
import random

class Padding(RequestField):
    name = 'padding'
    default = 0
    pattern = r'[a-zA-Z0-9\-_]+(?:\.[a-zA-Z0-9\-_]+)*'
    RANDOM_STRING = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    separate = 63
    def __str__(self):
        arr = [random.choice(self.RANDOM_STRING) for x in xrange(self.separate)]
        res = '.'.join([''.join(arr) for y in xrange(self.value)])
        res = res[:self.value]
        if res[-1:] == '.':
            res = res[:-1] + random.choice(self.RANDOM_STRING)
        return res
    def decode(self):
        return len(self.value)
