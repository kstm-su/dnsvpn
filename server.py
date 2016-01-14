#!/usr/bin/env python3

import time
from lib.tuntap import TunThread
from lib import dns
from lib import query
from lib.packet import Packet, PacketPool

hostname = b'vpn.bgpat.net'
query.Field.HostName.default = hostname
query.Field.HostName.pattern = hostname
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
        rxpool.push(pkt)


tun = VPNServer()
tun.start()


class DNSServer(dns.ServerThread):
    daemon = True

    def receive(self, req, addr, port, data):
        txInit = query.TxInitialize(req)
        txSend = query.TxSend(req)
        rxRecv = query.Receive(req)
        rxPoll = query.Polling(req)
        try:
            if txInit.params is not None:
                params = txInit.params
                res = self.txinit(params['id'], params['count'])
                print('txinit', params)
            elif txSend.params is not None:
                id = txSend.params['id']
                seq = txSend.params['sequence']
                res = self.txsend(id, seq, txSend.params['data'])
                print('txsend', params)
            elif rxRecv.params is not None:
                params = rxRecv.params
                res = self.rxrecv(params['id'], params['sequence'])
                print('rxrecv', params, req)
            elif rxPoll.params is not None:
                res = self.rxpoll()
                print('rxpoll')
            else:
                res = query.Error()
        except:
            res = query.Error()
            print('exception', req, addr, port, data.qd.__dict__)
        print('< ', res.__class__.__name__, res.params)
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
        return query.Ok(count=pkt.count, sequence=seq)

    def rxrecv(self, id, seq):
        global rxpool
        if id not in rxpool:
            print('recv error', id, seq)
            print('rxpool', list(rxpool.keys()))
            return query.Error()
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
