# -*- coding: utf-8 -*-
import fields
from request import *

class Initialize(Request):
    format = (fields.Count, fields.ID, fields.HostName, '')

class Send(Request):
    format = (fields.Data, fields.Sequence, fields.ID, fields.HostName, '')

class Ok(Request):
    format = (fields.DecCount, fields.DecSequence)

class Error(Request):
    format = ('0.0', fields.ErrorNo)

class ServerReader(Reader):
    classes = (Initialize, Send)

class ClientReader(Reader):
    classes = (Error, Ok)
