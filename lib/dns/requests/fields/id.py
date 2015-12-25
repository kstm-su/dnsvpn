# -*- coding: utf-8 -*-
from field import RequestField

class ID(RequestField):
    name = 'id'
    default = 0
    pattern = r'[0-9a-f][0-9a-f]\.[0-9a-f][0-9a-f]'
    def __str__(self):
        high = (self.value >> 8) & 0xff
        low = self.value & 0xff
	return '%02x.%02x' % (high, low)
    def decode(self):
        word = str(self.value).replace('.', '')
        return int(word, 16)
