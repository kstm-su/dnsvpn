# -*- coding: utf-8 -*-
from field import RequestField

class ErrorNo(RequestField):
    name = 'error'
    default = 0
    def __str__(self):
        high = (self.value >> 8) & 0xff
        low = self.value & 0xff
	return '%u.%u' % (high, low)
