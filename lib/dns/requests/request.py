# -*- coding: utf-8 -*-

class Request():
    format = None
    separator = '.'
    def __init__(self, **kwargs):
        self.data = []
        for x in self.format:
            if isinstance(x, str):
                self.data.append(x)
                continue
            if x.name in kwargs:
                self.data.append(x(kwargs[x.name]))
            else:
                self.data.append(x())
    def __str__(self):
        res = []
        for x in self.data:
            res.append(str(x))
        return self.separator.join(res)
