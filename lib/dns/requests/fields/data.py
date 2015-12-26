# -*- coding: utf-8 -*-
from field import RequestField


class Data(RequestField):
    name = 'data'
    pattern = r'[a-zA-Z0-9\-_]+(?:\.[a-zA-Z0-9\-_]+)*'
