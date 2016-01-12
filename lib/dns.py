import threading
import socket
import random
from scapy.all import DNS, DNSQR, DNSRR, DNSRROPT

TYPE = {
    'ANY': 0,
    'A': 1,
    'NS': 2,
    'MD': 3,
    'MF': 4,
    'CNAME': 5,
    'SOA': 6,
    'MB': 7,
    'MG': 8,
    'MR': 9,
    'NULL': 10,
    'WKS': 11,
    'PTR': 12,
    'HINFO': 13,
    'MINFO': 14,
    'MX': 15,
    'TXT': 16,
    'RP': 17,
    'AFSDB': 18,
    'SIG': 24,
    'KEY': 25,
    'AAAA': 28,
    'LOC': 29,
    'SRV': 33,
    'NAPTR': 35,
    'KX': 36,
    'CERT': 37,
    'A6': 38,
    'DNAME': 39,
    'OPT': 41,
    'APL': 42,
    'DS': 43,
    'SSHFP': 44,
    'IPSECKEY': 45,
    'RRSIG': 46,
    'NSEC': 47,
    'DNSKEY': 48,
    'DHCID': 49,
    'NSEC3': 50,
    'NSEC3PARAM': 51,
    'TLSA': 52,
    'HIP': 55,
    'CDS': 59,
    'CDNSKEY': 60,
    'TKEY': 249,
    'TSIG': 250,
    'IXFR': 251,
    'AXFR': 252,
    '*': 255,
    'CAA': 257,
    'TA': 32768,
    'DLV': 32769,
}


class ServerThread(threading.Thread):
    sock = None
    addr = '0.0.0.0'
    port = 53
    size = 4096
    protocol = 'UDP'
    timeout = 3
    backlog = 10

    def __init__(self):
        threading.Thread.__init__(self)
        if self.protocol == 'UDP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.addr, self.port))
        elif self.protocol == 'TCP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.addr, self.port))
            self.sock.listen(self.backlog)
        self.sock.settimeout(self.timeout)

    def run(self):
        while True:
            if self.protocol == 'UDP':
                data, client = self.sock.recvfrom(self.size)
            if self.protocol == 'TCP':
                conn, client = self.sock.accept()
                data = self.sock.recv(self.size)
            request = DNS(data)
            try:
                qname = request.qd.qname
            except:
                qname = None
            response = self.receive(qname, client[0], client[1], request)
            if not isinstance(response, DNS):
                response = self.makeResponse(request, **response)
            if self.protocol == 'UDP':
                self.sock.sendto(bytes(response), client)
            if self.protocol == 'TCP':
                conn.send(bytes(response))
                conn.close()

    def receive(self, req, addr, port, data):
        return {}

    def makeResponse(self, req, **kwargs):
        id = req.id
        ttl = kwargs.get('ttl', 1)
        rdata = kwargs.get('value', b'')
        rtype = TYPE[kwargs.get('type', 'A')]
        ans = DNSRR(rrname=req.qd.qname, ttl=ttl, rdata=rdata, type=rtype)
        return DNS(id=id, qr=1, qd=req.qd, an=ans, ar=req.ar)


class Client(object):
    sock = None
    addr = None
    port = 53
    size = 4096
    protocol = 'UDP'
    timeout = 3
    edns0 = False

    def __init__(self, **kwargs):
        self.addr = kwargs.get('addr', self.addr)
        self.port = kwargs.get('port', self.port)
        self.size = kwargs.get('size', self.size)
        self.protocol = kwargs.get('protocol', self.protocol)
        self.timeout = kwargs.get('timeout', self.timeout)
        self.edns0 = kwargs.get('edns0', self.edns0)
        if self.protocol == 'UDP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif self.protocol == 'TCP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            raise Exception('Not supported')
        self.sock.settimeout(self.timeout)
        if 'data' in kwargs:
            data = kwargs['data']
            if isinstance(data, DNS):
                self.data = data
            else:
                self.makeRequest(**data)
            self.send()

    def send(self):
        if self.protocol == 'UDP':
            self.sock.sendto(bytes(self.data), (self.addr, self.port))
        elif self.protocol == 'TCP':
            self.sock.connect((self.addr, self.port))
            self.sock.send(bytes(self.data))
        else:
            raise Exception('Not supported')
        # TODO バッファ不足時のループ書く
        res = self.sock.recv(self.size)
        if self.protocol == 'TCP':
            self.sock.close()
        self.response = DNS(res)
        self.answers = []
        x = self.response.an
        for i in range(self.response.ancount):
            rdata = x.rdata
            if isinstance(rdata, str):
                rdata = rdata.encode('utf8')
            self.answers.append(rdata)
            x = x.payload
        return res

    def makeRequest(self, **kwargs):
        id = kwargs.get('id', self.generateID())
        qname = kwargs.get('value', u'')
        qtype = kwargs.get('type', 1)
        if isinstance(qtype, str):
            qtype = TYPE[qtype]
        qd = DNSQR(qname=qname, qtype=qtype, qclass=1)
        ar = None
        if self.edns0:
            ar = DNSRROPT(rrname='.', type=TYPE['OPT'], rclass=self.size)
        request = DNS(id=id, rd=1, qd=qd, ar=ar)
        self.data = request

    def generateID(self):
        return random.randint(0, 0xffff)
