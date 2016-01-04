import re
import lib.field as Field


class Query(list):
    fields = ()
    separator = '.'

    def __init__(self, encoded=None, **kwargs):
        list.__init__(self)
        for field in self.fields:
            if isinstance(field, str):
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
            self.encoded = str(encoded)
            self.params = self.decode()

    def __bytes__(self):
        return self.encode().encode('utf-8')

    def __str__(self):
        return self.encode()

    def pattern(self, **kwargs):
        patterns = []
        for field in self.fields:
            if isinstance(field, str):
                pattern = re.escape(field)
            else:
                if field.name in kwargs:
                    value = re.escape(kwargs[field.name])
                else:
                    value = field.pattern
                pattern = '(?P<%s>%s)' % (field.name, value)
            patterns.append(pattern)
        return '^%s$' % re.escape(self.separator).join(patterns)

    def encode(self):
        return self.separator.join([str(field) for field in self])

    def decode(self):
        pattern = self.pattern(**self.params)
        matches = re.match(pattern, self.encoded)
        if matches is None:
            return None
        params = matches.groupdict()
        res = {}
        for field in self.fields:
            if isinstance(field, str):
                continue
            if field.name in params:
                value = params[field.name]
                res[field.name] = field(value).decode()
            else:
                res[field.name] = field.default
        return res


class Error(Query):
    fields = ('0.0', Field.ErrorNo)


class Polling(Query):
    fields = (Field.Padding, Field.HostName, '')


class RxInitialize(Query):
    fields = (Field.HexCount, Field.ID, Field.Data, Field.HostName, '')


class RxSend(Query):
    fields = (Field.HexSequence, Field.ID, Field.Data, Field.HostName, '')


class Receive(Query):
    fields = (Field.HexSequence, Field.ID, Field.Padding, Field.HostName, '')


class TxInitialize(Query):
    fields = (Field.HexCount, Field.ID, Field.HostName, '')


class TxSend(Query):
    fields = (Field.Data, Field.HexSequence, Field.ID, Field.HostName, '')


class Ok(Query):
    fields = (Field.DecimalCount, Field.DecimalSequence)

    def decode(self):
        res = Query.decode(self)
        if res['count'] == 0:
            return None
        return res
