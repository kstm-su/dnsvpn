#!/bin/bash
addr=192.168.200.2
server=`grep '^nameserver\s' /etc/resolv.conf | awk 'NR==1{print $2}'`
gw=`netostat -nr | grep -E '^(default|0\.0\.0\.0)' | awk 'NR==1{print $2}'`
ip r add $server via $gw
ip r delete default
./client.py
ip r add default via $gw
