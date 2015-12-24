# -*- coding: utf-8 -*-
from field import RequestField

class ID(RequestField):
    name = 'id'
    def __str__(self):
        high = (self.value >> 8) & 0xff
        low = self.value & 0xff
	return '%02x.%02x' % (high, low)
