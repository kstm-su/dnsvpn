#!/usr/bin/env python3

import base64
from scapy.all import IP


class Packet(dict):
    src = None
    hostname = ''
    size = 254
    separate = 63
    used = 11
    count = 0
    maxlen = size - used
    id = None

    def __init__(self, data, **kwargs):
        self.hostname = kwargs.get('hostname', self.hostname)
        self.size = kwargs.get('size', self.size)
        self.separate = kwargs.get('separate', self.separate)
        self.used = kwargs.get('used', self.used)
        self.maxlen = self.size - self.used - len(self.hostname)
        if isinstance(data, int):
            self.count = data
            return
        self.src = data
        self.pack()

    def pack(self):
        self.id = IP(self.src).id
        self.count = self.split()

    def unpack(self):
        buf = bytearray()
        for i in range(self.count):
            buf += self.decode(self[i])
        return bytes(buf)

    def split(self):
        src = self.encode(self.src)
        seq = 0
        buf = ''
        while len(src):
            sec = src[:self.separate]
            if len(buf) + len(sec) + 1 + self.used > self.maxlen:
                p = self.maxlen - len(buf) - self.used - 1
                buf += src[:p]
                src = src[p:]
                self[seq] = buf
                buf = ''
                seq += 1
            else:
                src = src[self.separate:]
                buf += sec + '.'
        if len(buf):
            self[seq] = buf[:-1]
            seq += 1
        return seq

    def encode(self, data):
        return base64.urlsafe_b64encode(data).decode('utf8').replace('=', '')

    def decode(self, data):
        data = data.replace('.', '')
        padding = '=' * ((4 - len(data) % 4) % 4)
        return base64.urlsafe_b64decode((data + padding).encode('utf8'))
