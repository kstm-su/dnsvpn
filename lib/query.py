import re
import lib.field as Field


class Query(list):
    fields = ()
    separator = b'.'
    params = None

    def __init__(self, encoded=None, **kwargs):
        list.__init__(self)
        for field in self.fields:
            if isinstance(field, bytes):
                self.append(field)
                continue
            if field.name in kwargs:
                value = kwargs[field.name]
                self.append(field(value))
            else:
                self.append(field())
        if encoded is None:
            self.params = kwargs
        else:
            self.encoded = bytes(encoded)
            self.params = self.decode(kwargs)

    def __bytes__(self):
        return self.encode()

    def __str__(self):
        return self.encode().decode('utf8')

    def pattern(self, **kwargs):
        patterns = []
        for field in self.fields:
            if isinstance(field, bytes):
                pattern = re.escape(field)
            else:
                if field.name in kwargs:
                    value = re.escape(kwargs[field.name])
                else:
                    value = field.pattern
                name = field.name.encode('utf8')
                pattern = b'(?P<%s>%s)' % (name, value)
            patterns.append(pattern)
        return b'^%s$' % re.escape(self.separator).join(patterns)

    def encode(self):
        return self.separator.join([bytes(field) for field in self])

    def decode(self, params=None):
        if params is None and self.params is not None:
            params = self.params
        pattern = self.pattern(**params)
        matches = re.match(pattern, self.encoded)
        if matches is None:
            return None
        groups = matches.groupdict()
        res = {}
        for field in self.fields:
            if isinstance(field, bytes):
                continue
            if field.name in groups:
                value = groups[field.name]
                res[field.name] = field(value).decode()
            else:
                res[field.name] = field.default
        return res


class Error(Query):
    fields = (b'0.0', Field.ErrorNo)
    type = 'A'


class Polling(Query):
    fields = (Field.Padding, Field.HostName, b'')
    type = 'A'


class RxInitialize(Query):
    fields = (Field.HexCount, Field.ID, Field.Data, b'')
    type = 'CNAME'


class RxSend(Query):
    fields = (Field.HexSequence, Field.ID, Field.Data, b'')
    type = 'CNAME'


class Receive(Query):
    fields = (Field.HexSequence, Field.ID, Field.Padding, Field.HostName, b'')
    type = 'A'


class TxInitialize(Query):
    fields = (Field.HexCount, Field.ID, Field.HostName, b'')
    type = 'A'


class TxSend(Query):
    fields = (Field.Data, Field.HexSequence, Field.ID, Field.HostName, b'')
    type = 'A'


class Ok(Query):
    fields = (Field.DecimalCount, Field.DecimalSequence)
    type = 'A'

    def decode(self, params={}):
        res = Query.decode(self, params)
        if res['count'] == 0:
            return None
        return res
