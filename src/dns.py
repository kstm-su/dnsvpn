#!/usr/bin/env python3

import threading
import socket
import random
from scapy.all import DNS, DNSQR, ls

TYPE = {
    'ANY': 0,
    'A': 1,
    'NS': 2,
    'MD': 3,
    'MF': 4,
    'CNAME': 5,
    'SOA': 6,
    'MB': 7,
    'MG': 8,
    'MR': 9,
    'NULL': 10,
    'WKS': 11,
    'PTR': 12,
    'HINFO': 13,
    'MINFO': 14,
    'MX': 15,
    'TXT': 16,
    'RP': 17,
    'AFSDB': 18,
    'AAAA': 28,
    'SRV': 33,
    'A6': 38,
    'DNAME': 39,
    'OPT': 41,
    'DS': 43,
    'RRSIG': 46,
    'NSEC': 47,
    'DNSKEY': 48,
    'NSEC3': 50,
    'NSEC3PARAM': 51,
    'ALL': 255,
    'DLV': 32769,
}


class ServerThread(threading.Thread):
    sock = None
    addr = '0.0.0.0'
    port = 53
    size = 4096

    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.addr, self.port))

    def run(self):
        while True:
            data, client = self.sock.recvfrom(self.size)
            response = self.receive(DNS(data), client[0], client[1])
            self.sock.sendto(bytes(response), client)

    def receive(self, data, addr, port):
        return data


class Client(object):
    sock = None
    addr = None
    port = 53
    size = 4096
    ext = False

    def __init__(self, **kwargs):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = kwargs.get('addr', self.addr)
        self.port = kwargs.get('port', self.port)
        self.size = kwargs.get('size', self.size)
        self.ext = kwargs.get('ext', self.ext)
        if 'data' in kwargs:
            data = kwargs['data']
            if isinstance(data, DNS):
                self.data = data
            else:
                self.makeRequest(**data)
            self.send()

    def send(self):
        self.sock.sendto(bytes(self.data), (self.addr, self.port))
        res = self.sock.recv(4096)
        self.response = DNS(res)
        return res

    def makeRequest(self, **kwargs):
        id = kwargs.get('id', self.generateID())
        qname = kwargs.get('value', u'')
        qtype = kwargs.get('type', 1)
        if isinstance(qtype, str):
            qtype = TYPE[qtype]
        qd = DNSQR(qname=qname, qtype=qtype, qclass=1)
        request = DNS(id=id, rd=1, qd=qd)
        ls(request)
        self.data = request

    def generateID(self):
        return random.randint(0, 0xffff)
