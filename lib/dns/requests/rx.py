# -*- coding: utf-8 -*-
import fields
from request import Request

class Receive(Request):
    format = (fields.Count, fields.ID, fields.HostName)
    separator = '.'
