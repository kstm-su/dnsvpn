#!/usr/bin/env python3

from scapy.all import IP, DNS, DNSRR, ls
from tuntap import TunThread
import dns
import query
from packet import Packet

hostname = 'vpn.bgpat.net'


class VPNServer(TunThread):
    daemon = True
    name = 'tun_server'
    addr = '192.168.200.1'
    gateway = '192.168.200.1'

    def receive(self, data):
        ls(IP(data))
        return
        # print(query.TxInitialize(hostname='localhost', id=IP(data).id))
        p = Packet(data, hostname='hoge.jp')
        dec = Packet(p.count)
        for q in p:
            dec[q] = p[q]
            print(q, p[q], len(dec))
        print(dec.count, ls(IP(dec.unpack())))


tun = VPNServer()
tun.start()
pool = {}


class DNSServer(dns.ServerThread):
    daemon = True

    def receive(self, req, addr, port):
        qname = req.qd.qname.decode('utf8')
        ini = query.TxInitialize(qname, hostname=hostname)
        params = ini.decode()
        if params is not None:
            pool[(addr, params['id'])] = Packet(params['count'])
            rdata = query.Ok(count=params['count'], sequence=params['count'])
        else:
            send = query.TxSend(qname, hostname=hostname)
            params = send.decode()
            if params is not None:
                pkt = pool[(addr, params['id'])]
                pkt[params['sequence']] = params['data']
                remain = pkt.count - len(pkt)
                if not remain:
                    tun.send(pkt.unpack())
                    ls(IP(pkt.unpack()))
                rdata = query.Ok(count=remain, sequence=params['sequence'])
        ans = DNSRR(rrname=req.qd.qname, ttl=1, rdata=bytes(rdata), type=1)
        res = DNS(id=req.id, qr=1, qd=req.qd, an=ans)
        return res


dnsd = DNSServer()
dnsd.start()

while True:
    None
