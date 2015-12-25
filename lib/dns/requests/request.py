# -*- coding: utf-8 -*-
import re

class Request():
    format = None
    pattern = ''
    separator = '.'
    def __init__(self, invert=False, **kwargs):
        self.data = []
        self.params = kwargs
        for x in self.format:
            if isinstance(x, str):
                self.data.append(x)
                continue
            if x.name in kwargs:
                if invert:
                    field = x(kwargs[x.name])
                    self.params[x.name] = field.decode()
                else:
                    self.data.append(x(kwargs[x.name]))
            else:
                self.data.append(x())
    def __str__(self):
        res = []
        for x in self.data:
            res.append(str(x))
        return self.separator.join(res)
    def pattern(self, **kwargs):
        res = [];
        for x in self.format:
            if isinstance(x, str):
                res.append(re.escape(x))
                continue
            pattern = x.pattern
            if x.name in kwargs:
                pattern = re.escape(kwargs[x.name])
            res.append('(?P<%s>%s)' % (x.name, pattern))
        separator = re.escape(self.separator)
        return '^%s$' % separator.join(res)


class Reader():
    classes = None
    separator = '.'
    def __init__(self, req, **kwargs):
        self.request = req
        self.params = None
        for x in self.classes:
            mobj = re.match(x().pattern(**kwargs), req)
            if mobj:
                kwargs = mobj.groupdict()
                req = x(True, **kwargs)
                self.type = x.__name__
                self.params = req.params
                return
