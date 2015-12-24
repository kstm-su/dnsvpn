# -*- coding: utf-8 -*-
import fields
from request import Request

class Initialize(Request):
    format = (fields.Data, fields.HostName)
    separator = '.'

class Receive(Request):
    format = (fields.Count, fields.ID, fields.HostName)
    separator = '.'
