# coding: UTF-8
import subprocess
import threading
import os
import socket
import random
import settings
from scapy.all import *
from lib import dns
from printpp import pprint

# ServerAddr and hostname
SERVER_ADDR = '160.252.88.2'
SERVER_HOSTNAME = 'v.fono.jp'
IF_NAME = 'tun1'
tun = os.open(TUN_PATH, os.O_RDWR)
subprocess.check_call('sudo ifconfig tun1 % % netmask 255.255.255.0 up', shell=True)

def genID():
    return random.randint(0, 0xffff)

class TunReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 
        client = socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        global tun
        while (True):
            data = os.read(tun, 1500)
            dl = dns.datalist.DataList(data, SERVER_HOSTNAME)
            data = IP(data)
            id = data.id
            packets = []
            count = len(dl)
            for x in xrange(count):
                record = dns.requests.tx.Send(data=dl[x], sequence=x, id=id, hostname=SERVER_HOSTNAME)
                qd = DNSQR(qname=str(record), qtype=dns.type.A, qclass=1)
                packets.append(DNS(id=genID(), rd=1, qd=qd))

            ls(packets[0])
	    
	    record = dns.requests.tx.Initialize(count=count, id=id, hostname=SERVER_HOSTNAME)
            qd = DNSQR(qnmme=str(record), qtype=dns.type.A, qclass=1)
            req = DNS(id=genID(), rd=1, qd=qd)
            client.sendto(str(req), (SERVER_ADDR, 53))

	    res = dns.requests.tx.ClientReader(str(client.recv(1024)), hostname=SERVER_HOSTNAME)
            if res.type == 'Ok':
                for p in packets:
                    client.sendto(str(p), (SERVER_ADDR, 53))
                    res = dns.requests.tx.ClientReader(str(client.recv(1024)), hostname=SERVER_HOSTNAME)
                    if res.type == 'Error':
                        break

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
