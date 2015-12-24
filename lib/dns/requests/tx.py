# -*- coding: utf-8 -*-
import fields
from request import Request

class Initialize(Request):
    format = (fields.Count, fields.ID, fields.HostName)
    separator = '.'

class Send(Request):
    format = (fields.Data, fields.Sequence, fields.ID, fields.HostName)
    separator = '.'
