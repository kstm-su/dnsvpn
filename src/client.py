#!/usr/bin/env python3

import time
from scapy.all import ls
from tuntap import TunThread
import dns
import query
from packet import Packet

addr = '192.168.33.10'
hostname = 'vpn.bgpat.net'


class VPNClient(TunThread):
    daemon = True
    name = 'tun_client'
    addr = '192.168.200.2'
    gateway = '192.168.200.1'

    def receive(self, data):
        pkt = Packet(data, hostname=hostname)
        # print(pkt)
        ini = query.TxInitialize(
            hostname=hostname,
            id=pkt.id,
            count=pkt.count
        )
        # print(ini)
        client = dns.Client(addr=addr, type='A', data={'value': bytes(ini)})
        if query.Error(client.response.an.rdata).decode() is not None:
            return
        res = query.Ok(client.response.an.rdata).decode()
        if res['count'] != res['sequence']:
            return
        # while len(pkt):
        seq = list(pkt.keys())[0]
        send = query.TxSend(data=pkt[seq], sequence=seq, id=pkt.id,
                            hostname=hostname)
        # print(send)
        data = {
            'value': bytes(send)
        }
        c = dns.Client(addr=addr, type='A', data=data)
        # print(c.response.an.rdata)


tun = VPNClient()
tun.start()
pool = {}


while True:
    poll = query.Polling(hostname=hostname, padding=253-len(hostname))
    cl = dns.Client(addr=addr, type='A', data={'value': bytes(poll)})
    rdata = cl.response.an.rdata
    if isinstance(rdata, bytes):
        rdata = rdata.decode('utf8')
    if query.Error(cl.response.an.rdata).decode() is not None:
        print('noop')
        time.sleep(1)
        continue
    while True:
        ls(cl.response)
        params = query.RxInitialize(rdata).decode()
        if params is not None and params['id'] not in pool:
            pkt = Packet(params['count'])
            id = params['id']
            pool[id] = pkt
            seq = 0
        else:
            id = params['id']
            pkt = pool[id]
            seq = params['sequence']
        pkt[seq] = params['data']
        if len(pkt) == pkt.count:
            tun.send(pkt.unpack())
            del pool[id]
            break
        recv = query.Receive(hostname=hostname, sequence=seq, id=id, padding=10)
        cl = dns.Client(addr=addr, type='A', data={'value': bytes(recv)})
