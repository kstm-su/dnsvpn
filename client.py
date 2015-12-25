import subprocess
import threading
import os
import time
import binascii
import base64
import socket
import random
from scapy.all import *
from lib import dns

tun = os.open('/dev/tun1', os.O_RDWR)
subprocess.check_call('sudo ifconfig tun1 10.10.0.2 10.10.0.2 netmask 255.255.255.0 up', shell=True)

# ServerAddr and hostname
SERVER_ADDR = '160.252.88.2'
SERVER_HOSTNAME = '4no.jp'

def genID():
    return random.randint(0, 0xffff)

class TunReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 


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
