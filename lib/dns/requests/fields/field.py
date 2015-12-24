# -*- coding: utf-8 -*-

class RequestField():
    name = None
    default = ''
    def __init__(self, *args):
        if len(args) > 0:
            self.value = args[0]
        else:
            self.value = self.default
    def __str__(self):
        return str(self.value)

class RequestFieldHostName(RequestField):
    name = 'hostname'
    default = '.'
    def __str__(self):
        return '%s.' % self.value

class RequestFieldId(RequestField):
    name = 'id'
    def __str__(self):
        return '%02x.%02x' % ((self.value >> 8) & 0xff, self.value & 0xff)

class RequestFieldSequence(RequestField):
    name = 'sequence'
    def __str__(self):
	return '%02x.%02x' % ((self.value >> 8) & 0xff, self.value & 0xff)

class RequestFieldCount(RequestField):
    name = 'count'
    default = 0
    def __str__(self):
        return '%02x.%02x' % ((self.value >> 8) & 0xff, self.value & 0xff)

class RequestFieldData(RequestField):
    name = 'data'
    default = ''

