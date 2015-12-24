# -*- coding: utf-8 -*-
from base64 import *

class DataList(list):
    def __init__(self, src, hostname='', size=254, separate=63, used=11):
        list.__init__(self)
        if isinstance(src, list):
            for x in src:
                self.append(x)
            self._join()
        else:
            self.src = src
            self.hostname = hostname
            self.size = size
            self.separate = separate
            self.used = used + len(self.hostname)
            self._split()
    def _split(self):
        src = urlsafe_b64encode(self.src).replace('=', '')
        remain = self.size - self.used
        seq = 0
        res = []
        buf = ''
        while len(src):
            section = src[:self.separate]
            if len(buf) + len(section) + 1 + self.used > self.size:
                p = self.size - len(buf) - self.used - 1
                buf += src[:p]
                src = src[p:]
                self.append(buf)
                buf = ''
                seq += 1
            else:
                src = src[self.separate:]
                buf += '%s.' % section
        if len(buf):
            self.append(buf[:-1])
            seq += 1
        self.count = seq
    def _join(self):
        src = ''.join(self).replace('.', '')
        self.src = urlsafe_b64decode(src)
