#!/usr/bin/env python3

import time
from lib.tuntap import TunThread
from lib import dns
from lib import query
from lib.packet import Packet, PacketPool
from lib.connection import Connection, ConnectionPool

addr = '192.168.33.10'
hostname = b'vpn.bgpat.net'
query.Field.HostName.default = hostname
query.Field.HostName.pattern = hostname
Packet.hostname = hostname

txpool = PacketPool()
rxpool = PacketPool()


class TxConnection(Connection):

    def main(self):
        init = query.TxInitialize(id=self.data.id, count=self.data.count)
        req = {
            'value': bytes(init),
            'type': init.type,
        }
        client = dns.Client(addr=addr, data=req)
        self.receive(client)

    def receive(self, client):
        if not len(client.answers):
            raise Exception('No answers')
        for ans in client.answers:
            ok = query.Ok(ans)
            if ok.params is None:
                continue
            count = ok.params['count']
            seq = ok.params['sequence']
            if seq < count:  # データ送信完了
                del self.data[seq]
                if not len(self.data):  # 全データ送信完了
                    return
        self.send()

    def send(self):
        i = list(self.data.keys())[0]
        req = query.TxSend(data=self.data[i], sequence=i, id=self.data.id)
        client = dns.Client(addr=addr, data={
            'value': bytes(req),
            'type': req.type,
        })
        self.receive(client)


txconn = ConnectionPool(TxConnection)
# rxconn = ConnectionPool(RxConnection)


class VPNClient(TunThread):
    daemon = True
    name = 'tun0'
    addr = '192.168.200.2'
    gateway = '192.168.200.1'

    def receive(self, data):
        global txpool
        pkt = Packet(data)
        txconn.push(pkt)


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
