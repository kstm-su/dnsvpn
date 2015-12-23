import subprocess
import threading
import os
import time
import binascii
import base64
from scapy.all import *

tun = os.open('/dev/tun1', os.O_RDWR)
subprocess.check_call('sudo ifconfig tun1 10.10.0.1 10.10.0.1 netmask 255.255.255.0 up', shell=True)

class TunReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 

    def run(self):
        global tun
        while (True):
           data = os.read(tun, 1500)
	   data = IP(data)
	   ls(data)
	   print data.id
	   data_base64 =  base64.urlsafe_b64encode(str(data))
	   print data_base64
	   print 'id_length : ' + str(data.id.bit_length() // 8)
	   print 'base64_length : ' + str(len(data_base64))

class TunWriter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global tun
        while(True):
            m = base64.urlsafe_b64decode(message)
            os.write(tun, m)

TunRXThread = TunReader()
TunRXThread.daemon = True
TunRXThread.start()

while True:
    time.sleep(1)
