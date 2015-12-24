# -*- coding: utf-8 -*-
from pprintpp import *

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

class Request():
    format = None
    separator = ''
    def __init__(self, **kwargs):
        self.data = []
        for x in self.format:
            self.data.append(x(kwargs[x.name]))
    def __str__(self):
        res = []
        for x in self.data:
            res.append(str(x))
        return self.separator.join(res)

class TXInitRequest(Request):
    format = (RequestFieldCount, RequestFieldId, RequestFieldHostName)
    separator = '.'

class TXRequest(Request):
    format = (RequestFieldData, RequestFieldSequence, RequestFieldId, RequestFileHostname)
    separator = '.'

class RXRequest(Request):
    format = (RequestFieldCount, RequestFieldID, RequestFiledHostname)
    separator '.'

tx = TXRequest(id = 1234, hostname = '4no.jp', count = 9876)
print str(tx)
