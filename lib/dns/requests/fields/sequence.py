# -*- coding: utf-8 -*-
from field import RequestField

class Sequence(RequestField):
    name = 'sequence'
    def __str__(self):
        high = (self.value >> 8) & 0xff
        low = self.value & 0xff
	return '%02x.%02x' % (high, low)
