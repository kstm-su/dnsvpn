# coding: UTF-8

import threading
import socket
import subprocess
import os
import struct
import Queue
import settings

from fcntl import ioctl
from scapy.all import *
from lib import dns
from pprintpp import pprint

queue = Queue.Queue()

class VPNServer(threading.Thread):
    TUNSETIFF = 0x400454ca
    TUNSETOWNER = TUNSETIFF + 2
    IFF_TUN = 0x0001
    IFF_TAP = 0x0002
    IFF_NO_PI = 0x1000
    def __init__(self):
        threading.Thread.__init__(self)
        self.tun = os.open(self.settings.TUN_PATH, os.O_RDWR)
        ifr = struct.pack('16sH', settings.IF_NAME, self.IFF_TUN | self.IFF_NO_PI)
        ioctl(self.tun, self.TUNSETIFF, ifr)
        ioctl(self.tun, self.TUNSETOWNER, 1000)
        subprocess.check_call('sudo ifconfig %s %s %s netmask 255.255.255.0 up' % (settings.IF_NAME, settings.GATEWAY_ADDR, settings.GATEWAY_ADDR), shell=True)
    def run(self):
        global queue
        while (True):
            packet = os.read(self.tun, 1500)
            id = IP(packet).id
            dl = dns.datalist.DataList(packet, '')
            count = len(dl)
            init = None
            data = []
            for x in xrange(count):
                if x:
                    init = dns.requests.rx.Send(data=dl[x], sequence=x, id=id)
                else:
                    data.append(dns.requests.rx.Initialize(data=dl[x], count=count, id=id))
            queue.put((init, data, id, count))

class DNSServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((settings.SERVER_ADDR, 53))
        #self.sock.bind(('0.0.0.0', 53))
    def run(self):
        global queue
        while (True):
            req, addr = self.sock.recvfrom(1024)
            req = DNS(req)
            #ls(req)
            if req.qd == None:
                continue
            if req.qd.qtype == dns.type.NS:
                rdata = settings.SERVER_ADDR
            else:
                rdata = '12.34.56.78'
                data = dns.requests.rx.ServerReader(str(req.qd.qdata), settings.SERVER_HOSTNAME)
                pprint(data)
            ans = DNSRR(rrname=req.qd.qname, ttl=1, rdata=rdata, type=req.qd.qtype)
            res = DNS(id=req.id, qr=1, qd=req.qd, an=ans)
            self.sock.sendto(str(res), addr)

th = DNSServer()
th.daemon = True
th.start()

while (True):
    0
