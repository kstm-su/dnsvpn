#!/usr/bin/env python3

import time
from lib.tuntap import TunThread
from lib import dns
from lib import query
from lib.packet import Packet, PacketPool

hostname = b'vpn.bgpat.net'
query.Field.HostName.default = hostname
Packet.hostname = hostname

txpool = PacketPool()
rxpool = PacketPool()


class VPNServer(TunThread):
    daemon = True
    name = 'tun0'
    addr = '192.168.200.1'
    gateway = '192.168.200.1'

    def receive(self, data):
        global rxpool
        pkt = Packet(data)
        rxpool.put(pkt)


tun = VPNServer()
tun.start()


class DNSServer(dns.ServerThread):
    daemon = True

    def receive(self, req, addr, port, data):
        txInit = query.TxInitialize(req)
        txSend = query.TxSend(req)
        rxRecv = query.Receive(req)
        rxPoll = query.Polling(req)
        if txInit is not None:
            res = self.txinit(txInit['id'], txInit['count'])
        elif txSend is not None:
            res = self.txsend(txSend['id'], txSend['sequence'], txSend['data'])
        elif rxRecv is not None:
            res = self.rxrecv(rxRecv['id'], rxRecv['sequence'])
        elif rxPoll is not None:
            res = self.rxpoll()
        else:
            res = query.Error()
        return {
            'value': bytes(res),
            'type': res.type,
        }

    def txinit(self, id, count):
        global txpool
        txpool[id] = Packet(count)
        return query.Ok(count=count, sequence=count)

    def txsend(self, id, seq, data):
        global txpool
        pkt = txpool[id]
        pkt[seq] = data
        remain = pkt.count - len(pkt)
        if not remain:
            tun.send(pkt.unpack())
            del txpool[id]
        return query.Ok(count=remain, sequence=seq)

    def rxrecv(self, id, seq):
        global rxpool
        pkt = rxpool[id]
        if seq in pkt:
            del pkt[seq]
        keys = list(pkt.keys())
        if len(keys):
            i = keys[0]
            return query.RxSend(data=pkt[i], sequence=i, id=id)
        else:
            del rxpool[id]
            return query.Error()

    def rxpoll(self):
        global rxpool
        if rxpool.empty():
            return query.Error()
        pkt = rxpool.front()
        if pkt.id in rxpool:
            return query.Error()
        rxpool[pkt.id] = pkt
        rxpool.pop()
        return query.RxInitialize(data=pkt[0], count=pkt.count, id=pkt.id)


dnsd = DNSServer()
dnsd.start()

while True:
    time.sleep(1)
