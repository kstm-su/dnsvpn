# coding: UTF-8

import threading
from scapy.all import *
from base64 import *

class PacketSniffer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while (True):
            frame = sniff(count = 1)[0]
            if not frame.haslayer(IP):
                continue
            packet = frame.getlayer(IP)
            data = urlsafe_b64encode(str(packet))
            print "%d %s" % (packet.id, data)

th = PacketSniffer()
th.daemon = True
th.start()

while (True):
    0
