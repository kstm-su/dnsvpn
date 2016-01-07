#!/usr/bin/env python3

import time
from lib.tuntap import TunThread
from lib import dns
from lib import query
from lib.packet import Packet, PacketPool

# addr = '127.0.0.1'
addr = '192.168.33.10'
hostname = b'vpn.bgpat.net'
query.Field.HostName.default = hostname
query.Field.HostName.pattern = hostname
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
            # for ans in client.answers:
            if not len(client.answers):
                return
            ans = client.answers[0]
            ok = query.Ok(ans)
            if ok.params is None:
                return
            count = ok.params['count']
            seq = ok.params['sequence']
            if seq < count:
                print('count = %d, seq = %d' % (count, seq), pkt)
                del pkt[seq]
                if not len(pkt):
                    return
            i = list(pkt.keys())[0]
            req = query.TxSend(data=pkt[i], sequence=i, id=pkt.id)
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
        # for ans in client.answers:
        ans = client.answers[0]
        rxInit = query.RxInitialize(ans)
        rxSend = query.RxSend(ans)
        if rxInit.params is not None and id not in rxpool:
            count = rxInit.params['count']
            id = rxInit.params['id']
            pkt = Packet(count)
            rxpool[id] = pkt
            seq = 0
            data = rxInit.params['data']
            print('rxinit', pkt.count, len(pkt))
        elif rxSend.params is not None:
            print('rxsend', pkt.count, len(pkt))
            id = rxSend.params['id']
            seq = rxSend.params['sequence']
            if id not in rxpool:
                break
                # raise 'packet is not found'
            pkt = rxpool[id]
            data = rxSend.params['data']
        else:
            break
        pkt[seq] = data
        if len(pkt) == pkt.count:
            tun.send(pkt.unpack())
            del rxpool[id]
            break
        req = query.Receive(sequence=seq, id=id, padding=16)
        print('recv', req)
        client = dns.Client(addr=addr, data={
            'value': bytes(req),
            'type': req.type,
        })
