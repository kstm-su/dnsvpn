#!/usr/bin/env python3

import time
from queue import Queue
from scapy.all import IP, DNS, DNSRR, ls
from tuntap import TunThread
import dns
import query
from packet import Packet

hostname = 'vpn.bgpat.net'


class PacketPool(Queue, dict):

    def Nop(self):
        return None


rxpool = PacketPool()
txpool = PacketPool()


class VPNServer(TunThread):
    daemon = True
    name = 'tun_server'
    addr = '192.168.200.1'
    gateway = '192.168.200.1'

    def receive(self, data):
        global rxpool
        pkt = Packet(data, hostname=hostname)
        rxpool.put(pkt)


tun = VPNServer()
tun.start()


class DNSServer(dns.ServerThread):
    daemon = True

    def receive(self, req, addr, port):
        global rxpool, txpool
        qname = req.qd.qname.decode('utf8')
        ini = query.TxInitialize(qname, hostname=hostname)
        params = ini.decode()
        if params is not None:
            txpool[(addr, params['id'])] = Packet(params['count'])
            rdata = query.Ok(count=params['count'], sequence=params['count'])
            ans = DNSRR(rrname=req.qd.qname, ttl=1, rdata=bytes(rdata), type=1)
            res = DNS(id=req.id, qr=1, qd=req.qd, an=ans)
            return res
        send = query.TxSend(qname, hostname=hostname)
        params = send.decode()
        if params is not None:
            pkt = txpool[(addr, params['id'])]
            pkt[params['sequence']] = params['data']
            remain = pkt.count - len(pkt)
            if not remain:
                tun.send(pkt.unpack())
                # ls(IP(pkt.unpack()))
                del txpool[(addr, params['id'])]
            rdata = query.Ok(count=remain, sequence=params['sequence'])
            ans = DNSRR(rrname=req.qd.qname, ttl=1, rdata=bytes(rdata), type=1)
            res = DNS(id=req.id, qr=1, qd=req.qd, an=ans)
            return res
        poll = query.Polling(qname, hostname=hostname)
        params = poll.decode()
        if params is not None:
            print('Polling', rxpool.qsize())
            if rxpool.qsize() < 1:
                rdata = query.Error()
                rtype = 1
            else:
                pkt = rxpool.get()
                rxpool[pkt.id] = pkt
                rdata = query.RxInitialize(data=pkt[0], count=pkt.count, id=pkt.id)
                rxpool.task_done()
                rtype = 5
            print(rdata, rtype)
            ans = DNSRR(rrname=req.qd.qname, ttl=1, rdata=bytes(rdata), type=rtype)
            res = DNS(id=req.id, qr=1, qd=req.qd, an=ans)
            return res
        recv = query.Receiv(qname, hostname=hostname)
        params = recv.decode()
        print('recv', params)
        if params is not None:
            rxpool[params['id']] = pkt
            if params['sequence'] in pkt:
                del pkt[params['sequence']]
            seq = list(pkt.keys())
            if len(seq) == 0:
                del rxpool[params['id']]
                rdata = query.Error()
                rtype = 1
            else:
                seq = seq[0]
                rdata = query.RxSend(data=pkt[seq], sequence=seq, id=pkt.id)
                rtype = 5
            ans = DNSRR(rrname=req.qd.qname, ttl=1, rdata=bytes(rdata), type=rtype)
            res = DNS(id=req.id, qr=1, qd=req.qd, an=ans)
            return res


dnsd = DNSServer()
dnsd.start()

while True:
    time.sleep(1)
