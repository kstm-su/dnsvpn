import socket
import random
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

# 問い合わせ先アドレス
SERVER_ADDR = '8.8.8.8'

def id():
    return random.randint(0, 0xffff)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
q = DNSQR(qname='aaa.vpn.bgpat.net.', qtype=TYPE.A, qclass=1)
req = DNS(id=id(), rd=1, qd=q)
ls(req)
client.sendto(str(req), (SERVER_ADDR, 53))
res = client.recv(1024)
ls(DNS(res))
