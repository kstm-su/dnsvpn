# -*- coding: utf-8 -*-

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
