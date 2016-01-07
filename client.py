#!/usr/bin/env python3

import time
from lib.tuntap import TunThread
from lib import dns
from lib import query
from lib.packet import Packet, PacketPool

addr = '127.0.0.1'
hostname = b'vpn.bgpat.net'
query.Field.HostName.default = hostname
Packet.hostname = hostname

txpool = PacketPool()
rxpool = PacketPool()


class VPNClient(TunThread):
    daemon = True
    name = 'tun0'
    addr = '192.168.200.2'
    gateway = '192.168.200.1'

    def receive(self, data):
        pkt = Packet(data)
        init = query.TxInitialize(id=pkt.id, count=pkt.count)
        client = dns.Client(addr=addr, data={
            'value': bytes(init),
            'type': init.type,
        })
        if client.answers is None:
            raise 'no answer'
        while len(pkt):
            for ans in client.answers:
                ok = query.Ok(ans)
                count = ok['count']
                seq = ok['sequence']
                if count != seq:
                    del pkt[seq]
                    if not len(pkt):
                        return
                i = list(pkt.keys())[0]
                req = query.TxSend(data=pkt[i], sequence=seq, id=pkt.id)
                data = {
                    'value': bytes(req),
                    'type': req.type
                }
                client = dns.Client(addr=addr, data=data)


tun = VPNClient()
tun.start()


while True:
    time.sleep(0.5)
    req = query.Polling(padding=16)
    client = dns.Client(addr=addr, data={
        'value': bytes(req),
        'type': req.type,
    })
    if client.answers is None:
        raise 'no answer'
        continue
    for ans in client.answers:
        err = query.Error(ans)
        if err is not None:
            continue
    while True:
        for ans in client.answers:
            rxInit = query.RxInitialize(ans)
            rxSend = query.RxSend(ans)
            if rxInit is not None:
                count = rxInit['count']
                id = rxInit['id']
                pkt = Packet(count)
                rxpool[id] = pkt
                seq = 0
                data = rxInit['data']
            elif rxSend is not None:
                id = rxSend['id']
                seq = rxSend['sequence']
                if id not in rxpool:
                    raise 'packet is not found'
                pkt = rxpool[id]
                data = rxSend['data']
            else:
                break
            pkt[seq] = data
            if len(pkt) == pkt.count:
                tun.send(pkt.unpack())
                del rxpool[id]
                break
        req = query.Receive(sequence=seq, id=id, padding=16)
        client = dns.Client(addr=addr, data={
            'value': bytes(req),
            'type': req.type,
        })
