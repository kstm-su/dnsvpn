import subprocess
import threading
import os
import time
import binascii
from scapy.all import *

tap = os.open('/dev/tun1', os.O_RDWR)
subprocess.check_call('sudo ifconfig tun1 10.10.0.1 10.10.0.1 netmask 255.255.255.0 up', shell=True)

class TapReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 

    def run(self):
        global tap
        while (True):
           data = os.read(tap, 1500)
	   ls(IP(data))
           print binascii.hexlify(data)

# os.write(tap, m)
TapThread = TapReader()
TapThread.daemon = True
TapThread.start()

while True:
    time.sleep(1)
