from lib.dns import requests
from pprintpp import pprint

req = requests.tx.Initialize(count = 1000, id = 1000, hostname = '4no.jp')
print req.__class__.__name__
print req
res = requests.tx.ClientReader(str(req), hostname='4no.jp')
pprint(res.params)
print 'class = %s\n' % res.type

req = requests.tx.Send(data = 'hogehoge', sequence = 12, id = 1000, hostname = '4no.jp')
print req.__class__.__name__
print req
res = requests.tx.ClientReader(str(req), hostname='4no.jp')
pprint(res.params)
print 'class = %s\n' % res.type

req = requests.tx.Ok(count = 100, sequence = 43)
print req.__class__.__name__
print req
res = requests.tx.ServerReader(str(req))
pprint(res.params)
print 'class = %s\n' % res.type

req = requests.tx.Error(error = 900)
print req.__class__.__name__
print req
res = requests.tx.ServerReader(str(req))
pprint(res.params)
print 'class = %s\n' % res.type

req = requests.rx.Polling(padding = 10, hostname = '4no.jp')
print req.__class__.__name__
print req
res = requests.rx.ClientReader(str(req), hostname='4no.jp')
pprint(res.params)
print 'class = %s\n' % res.type

req = requests.rx.Receive(padding = 70, sequence = 43, id = 101, hostname = '4no.jp')
print req.__class__.__name__
print req
res = requests.rx.ClientReader(str(req), hostname='4no.jp')
pprint(res.params)
print 'class = %s\n' % res.type

req = requests.rx.Initialize(data = 'hogehoge', count = 12, id = 1000)
print req.__class__.__name__
print req
res = requests.rx.ServerReader(str(req))
pprint(res.params)
print 'class = %s\n' % res.type

req = requests.rx.Send(data = 'aA0-_', sequence = 1, id = 1000)
print req.__class__.__name__
print req
res = requests.rx.ServerReader(str(req))
pprint(res.params)
print 'class = %s\n' % res.type

req = requests.rx.Error(error = 900)
print req.__class__.__name__
print req
res = requests.rx.ServerReader(str(req))
pprint(res.params)
print 'class = %s\n' % res.type
