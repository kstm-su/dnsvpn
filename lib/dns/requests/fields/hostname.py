# -*- coding: utf-8 -*-
from field import RequestField

class HostName(RequestField):
    name = 'hostname'
    default = '.'
    def __str__(self):
        return '%s.' % self.value
