import subprocess
import threading
import os
import time
import binascii
import base64
import socket
import random
from scapy.all import *

tun = os.open('/dev/tun1', os.O_RDWR)
subprocess.check_call('sudo ifconfig tun1 10.10.0.1 10.10.0.1 netmask 255.255.255.0 up', shell=True)

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

# ServerAddr and hostname
SERVER_ADDR = '8.8.8.8'
SERVER_HOSTNAME = 'vpn.bgpat.net'

def id()
    return random.randint(0, 0xffff)

class TunReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 


    def run(self):
        global tun
        while (True):
           data = os.read(tun, 1500)
	   data = IP(data)
	   ls(data)
	   print data.id
	   data_base64 =  base64.urlsafe_b64encode(str(data))
	   print data_base64
	   print 'id_length : ' + str(data.id.bit_length() // 8)
	   print 'base64_length : ' + str(len(data_base64))

           count = ceil(id_length // data_length)
           query = str(count) + '.' + data.id + '.' + SERVER_HOSTNAME + '.'
	   client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	   q = DNSQR(qname=query, qtype=TYPE.A, qclass=1)
	   req = DNS(id=id(), rd=1, qd=q)
           ls(req)
           client.sendto(str(req),(SERVER_ADDR,53))
           res = client.recv(1024)
           ls(DNS(res))

class TunWriter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global tun
        while(True):
            m = base64.urlsafe_b64decode(message)
            os.write(tun, m)

TunRXThread = TunReader()
TunRXThread.daemon = True
TunRXThread.start()

while True:
    time.sleep(1)
