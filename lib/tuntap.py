#!/usr/bin/env python3

import os
import subprocess
import threading
import fcntl
from lib import linux


class TunTapThread(threading.Thread):
    tun = None
    dev = None
    path = None
    name = None
    flags = linux.IFF_NO_PI
    addr = '192.168.120.1'
    gateway = '192.168.120.1'
    netmask = '255.255.255.0'
    mtu = 1500
    uid = None
    sysname = os.uname().sysname
    isLinux = sysname == 'Linux'
    isMacOSX = sysname == 'Darwin'

    def __init__(self):
        threading.Thread.__init__(self)
        if self.path is None:
            if self.isLinux:
                self.path = '/dev/net/' + self.dev
            elif self.isMacOSX:
                self.path = '/dev/' + self.name
        self.open()

    def open(self):
        self.tun = os.open(self.path, os.O_RDWR)
        if self.isLinux:
            if self.dev == 'tun':
                self.flags |= linux.TUN_TUN_DEV
            elif self.dev == 'tap':
                self.flags |= linux.TUN_TAP_DEV
            ifr = linux.ifreq(name=self.name.encode('utf8'), flags=self.flags)
            fcntl.ioctl(self.tun, linux.TUNSETIFF, ifr)
            if self.uid is not None:
                fcntl.ioctl(self.tun, linux.TUNSETOWNER, self.uid)
        self.ifup()

    def calcNetwork(self):
        addr = [int(i) for i in self.addr.split('.')]
        mask = [int(i) for i in self.netmask.split('.')]
        return '.'.join(str(addr[i] & mask[i]) for i in range(4))

    def ifup(self):
        option = {
            'name': self.name,
            'addr': self.addr,
            'gateway': self.gateway,
            'netmask': self.netmask,
            'network': self.calcNetwork(),
        }
        if self.isLinux:
            cmd = 'sudo ifconfig {name} {addr} netmask {netmask} up'
            subprocess.check_call(cmd.format(**option), shell=True)
            cmd = 'sudo route add -net {network} netmask {netmask} gw {gateway}'
            subprocess.check_call(cmd.format(**option), shell=True)
        if self.isMacOSX:
            cmd = 'sudo ifconfig {name} {addr} {gateway} netmask {netmask} up'
            subprocess.check_call(cmd.format(**option), shell=True)

    def run(self):
        while (True):
            data = os.read(self.tun, self.mtu)
            self.receive(data)

    def receive(self, data):
        return

    def send(self, data):
        os.write(self.tun, data)


class TunThread(TunTapThread):
    dev = 'tun'
    name = 'tun0'


class TapThread(TunTapThread):
    dev = 'tap'
    name = 'tap0'
