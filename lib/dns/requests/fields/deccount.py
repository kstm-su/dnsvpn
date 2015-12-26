# -*- coding: utf-8 -*-
from field import RequestField


class DecCount(RequestField):
    name = 'count'
    default = 0
    pattern = r'\d+\.\d+'

    def __str__(self):
        high = (self.value >> 8) & 0xff
        low = self.value & 0xff
        return '%u.%u' % (high, low)

    def decode(self):
        word = str(self.value).split('.')
        return (int(word[0]) << 8) | int(word[1])
