# -*- coding: utf-8 -*-

import base64

a = base64.urlsafe_b64encode("awtytewtartawrtaawaetewrasreoiaeaiopheariopghnstioprjgpawojyrgp@sejh[p@rsenhwajgh[ptsohj[areopgnjp[afohjeariopghareipgn[arpg"*3).replace('=','')
a += '0'*34
print a
n63 = 63
domain = "4no.jp"
domainlen = len(domain) #ドメインの長さ
usedlen = domainlen + 3 + 4 + 4 #すでに使われている長さ。ドット(1)*3、seq(4)、id(4)
count = (len(a) + (254 - usedlen - 1)) // (254 - usedlen) #何個返すか

seq = 0
pid = 123
c=""

while len(a)!=0:
    b = a[0:n63]
    if len(c) + len(b) + 1 + usedlen > 254:
        xxx = '%s%04x.%04x.%s.' % (c, seq, pid, domain)
        c += a[0:254-len(xxx)-1] + "."
	a = a[254-len(xxx)-1:]
	print '%s%04x.%04x.%s.' % (c, seq, pid, domain)
	c = ""
        seq += 1
    else:
	a = a[n63:]
   	c += b + "."

if len(c)!=0:
	print'%s%04x.%04x.%s.' % (c, seq, pid, domain)
	seq += 1
print seq
