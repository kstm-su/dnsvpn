# -*- coding: utf-8 -*-

class RequestField():
    name = None
    default = ''
    pattern = ''
    def __init__(self, *args):
        if len(args) > 0:
            self.value = args[0]
        else:
            self.value = self.default
    def __str__(self):
        return str(self.value)
    def decode(self):
        return self.value
