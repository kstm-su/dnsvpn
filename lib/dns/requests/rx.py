# -*- coding: utf-8 -*-
import fields
from request import Request

class Polling(Request):
    format = (fields.Padding, fields.HostName)

class Send(Request):
    format = (fields.Count, fields.ID, fields.Data)

class Receive(Request):
    format = (fields.Padding, fields.Sequence, fields.ID, fields.HostName)

class Error(Request):
    format = ('0.0', fields.ErrorNo)
