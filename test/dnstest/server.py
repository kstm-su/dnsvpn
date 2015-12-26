# coding: UTF-8

import socket
#from binascii import *
from scapy.all import *

class TYPE:
    ANY = 0
    A = 1
    NS = 2
    MD = 3
    MF = 4
    CNAME = 5
    SOA = 6
    MB = 7
    MG = 8
    MR = 9
    NULL = 10
    WKS = 11
    PTR = 12
    HINFO = 13
    MINFO = 14
    MX = 15
    TXT = 16
    RP = 17
    AFSDB = 18
    AAAA = 28
    SRV = 33
    A6 = 38
    DNAME = 39
    OPT = 41
    DS = 43
    RRSIG = 46
    NSEC = 47
    DNSKEY = 48
    NSEC3 = 50
    NSEC3PARAM = 51
    ALL = 255
    DLV = 32769

# NSレコードで返すIPアドレス
SERVER_ADDR = '27.96.45.147'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_ADDR, 53))
try:
    while (True):
        req, addr = server.recvfrom(1024)
        req = DNS(req)
        ls(req)
        if req.qd == None:
            continue
        if req.qd.qtype == TYPE.NS:
            rdata = SERVER_ADDR
        else:
            rdata = '12.34.56.78'
        ans = DNSRR(rrname=req.qd.qname, ttl=0, rdata=rdata, type=req.qd.qtype)
        txt = DNSRR(rrname=req.qd.qname, ttl=0, rdata='hoge', type=TYPE.TXT)
        txt = txt/DNSRR(rrname=req.qd.qname, ttl=0, rdata='hoge', type=TYPE.TXT)
        res = DNS(id=req.id, qr=1, qd=req.qd, an=ans/txt)
        server.sendto(str(res), addr)
except:
    server.close()
