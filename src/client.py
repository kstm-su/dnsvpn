#!/usr/bin/env python3

import time
from scapy.all import IP, ls
from tuntap import TunThread
import dns
import query
from packet import Packet

# addr = '192.168.33.10'
# addr = '8.8.8.8'
# addr = '27.120.111.8'
addr = '160.252.88.2'
hostname = 'vpn.bgpat.net'

dns.Client.ext = True


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
        print('initialize', ini, ini.__dict__)
        client = dns.Client(addr=addr, type='A', data={'value': bytes(ini)})
        while len(pkt):
            rdata = client.response.an.rdata
            if isinstance(rdata, bytes):
                rdata = rdata.decode('utf8')
            if query.Error(rdata).decode() is not None:
                return
            res = query.Ok(rdata).decode()
            if res['count'] != res['sequence']:
                del pkt[res['sequence']]
                if len(pkt) == 0:
                    return
            seq = list(pkt.keys())[0]
            send = query.TxSend(data=pkt[seq], sequence=seq, id=pkt.id,
                                hostname=hostname)
            data = {
                'value': bytes(send)
            }
            print('send', send, send.__dict__)
            client = dns.Client(addr=addr, type='A', data=data)


tun = VPNClient()
tun.start()
pool = {}


while True:
    poll = query.Polling(hostname=hostname, padding=252-len(hostname))
    print(poll)
    cl = dns.Client(addr=addr, type='A', data={'value': bytes(poll)})
    try:
        rdata = cl.response.an.rdata
        if isinstance(rdata, bytes):
            rdata = rdata.decode('utf8')
    except:
        print('except: ')
        ls(cl.response)
        continue
    print('rdata', rdata)
    if query.Error(cl.response.an.rdata).decode() is not None:
        print('noop')
        time.sleep(0.5)
        continue
    while True:
        params = query.RxInitialize(rdata, hostname=hostname).decode()
        print('recv', rdata, pool)
        if params is not None and params['id'] not in pool:
            pkt = Packet(params['count'])
            id = params['id']
            pool[id] = pkt
            seq = 0
        else:
            params = query.RxSend(rdata, hostname=hostname).decode()
            print('rx send', params, rdata)
            id = params['id']
            pkt = pool[id]
            seq = params['sequence']
        pkt[seq] = params['data']
        print('recv pkt', pkt.__dict__, len(pkt), pkt)
        if len(pkt) == pkt.count:
            # ls(IP(pkt.unpack()))
            tun.send(pkt.unpack())
            del pool[id]
            break
        recv = query.Receive(hostname=hostname, sequence=seq, id=id, padding=10)
        cl = dns.Client(addr=addr, type='A', data={'value': bytes(recv)})
        rdata = cl.response.an.rdata
        if isinstance(rdata, bytes):
            rdata = rdata.decode('utf8')
