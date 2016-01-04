import string
from random import choice as rand


class QueryField(object):
    name = None  # field name
    default = ''
    pattern = ''

    def __init__(self, value=None):
        if value is None:
            self.value = self.default
        else:
            self.value = value

    def __str__(self):
        return str(self.encode())

    def encode(self):
        return self.value

    def decode(self):
        return self.value


class ShortHex(QueryField):
    default = 0
    pattern = r'[0-9a-f][0-9a-f]\.[0-9a-f][0-9a-f]'

    def encode(self):
        high = (self.value >> 8) & 0xff
        low = self.value & 0xff
        return '%02x.%02x' % (high, low)

    def decode(self):
        hex_ = str(self.value).replace('.', '')
        return int(hex_, 16)


class ShortDecimal(QueryField):
    default = 0
    pattern = r'[0-9]+\.[0-9]+'

    def encode(self):
        high = (self.value >> 8) & 0xff
        low = self.value & 0xff
        return '%d.%d' % (high, low)

    def decode(self):
        decimal = str(self.value).split('.')
        high = int(decimal[0]) << 8
        low = int(decimal[1])
        return high | low


class DomainString(QueryField):
    pattern = r'[a-zA-Z0-9\-_]+(?:\.[a-zA-Z0-9\-_]+)*'


class ID(ShortHex):
    name = 'id'


class HexCount(ShortHex):
    name = 'count'


class DecimalCount(ShortDecimal):
    name = 'count'


class HexSequence(ShortHex):
    name = 'sequence'


class DecimalSequence(ShortDecimal):
    name = 'sequence'


class Data(DomainString):
    name = 'data'


class HostName(DomainString):
    name = 'hostname'


class Padding(DomainString):
    name = 'padding'
    default = 0
    length = 63
    RANDOM_STRING = string.ascii_letters + string.digits + '-_'

    def encode(self):
        rows = (self.value + self.length) // self.length
        padding = []
        for i in range(rows):
            row = [rand(self.RANDOM_STRING) for i in range(self.length)]
            padding.append(''.join(row))
        res = '.'.join(padding)[:self.value]
        if res[-1:] == '.':
            return '%s.%s' % (res[:-2], res[-2])
        return res

    def decode(self):
        return len(self.value)


class ErrorNo(ShortDecimal):
    name = 'error'
