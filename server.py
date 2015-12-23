from scapy.all import *
import binascii
import threading
from pprintpp import pprint

#server = '10.0.3.203'
#client = '10.10.0.1'

class PacketSniffer(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
        def run(self):
                while (True):
                        frame = sniff(count = 1)
                        frame = frame[0]
                        if not frame.haslayer(IP):
                                continue
                        packet = frame.getlayer(IP)
                        #ls(packet)
                        pprint(packet)
                        print binascii.hexlify(str(packet))

th = PacketSniffer()
th.daemon = True
th.start()

while (True):
        packet = binascii.unhexlify(raw_input())
        eth = Ether(packet)
        ip = eth.getlayer(IP)
        #ip[IP].src = server
        #del ip.chksum
        #if ip.haslayer(ICMP):
        #       del ip[ICMP].chksum
        #if ip.haslayer(TCP):
        #       del ip[TCP].chksum
        #if ip.haslayer(UDP):
        #       del ip[UDP].chksum
        ls(ip)
        send(ip)
