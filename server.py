# coding: UTF-8

import threading
import socket
from scapy.all import *
from base64 import *
from binascii import *
from lib import dns

SERVER_ADDR = '27.96.45.147'

class DNSServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.bind(SERVER_ADDR, 53)
        self.sock.bind(('0.0.0.0', 53))
    def run(self):
        while (True):
            req, addr = self.sock.recvfrom(1024)
            req = DNS(req)
            ls(req)
            if req.qd == None:
                continue
            if req.qd.qtype == dns.type.NS:
                rdata = SERVER_ADDR
            elif req.qd.qtype == dns.type.SOA:
                rdata = '\x034no\x02jp\x00\x034no\x02jp\x00\x00\xff\xff\xff\x00\x00\xff\xff\x00\x00\x0e\x10\x00\x00\x0e\x10\x00\x00\x0e\x10'
            else:
                rdata = '12.34.56.78'
            ans = DNSRR(rrname=req.qd.qname, ttl=0, rdata=rdata, type=req.qd.qtype)
            res = DNS(id=req.id, qr=1, qd=req.qd, an=ans)
            self.sock.sendto(str(res), addr)

th = DNSServer()
th.daemon = True
th.start()

while (True):
    0
