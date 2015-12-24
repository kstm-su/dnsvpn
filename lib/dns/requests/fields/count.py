# -*- coding: utf-8 -*-
from field import RequestField

class Count(RequestField):
    name = 'count'
    default = 0
    def __str__(self):
        high = (self.value >> 8) & 0xff
        low = self.value & 0xff
	return '%02x.%02x' % (high, low)
