from lib.dns import requests
from pprintpp import pprint

req = requests.tx.Initialize(count = 1000, id = 1000, hostname = '4no.jp')
print req
res = requests.tx.ClientReader(str(req), hostname='4no.jp')
pprint(res.params)

req = requests.tx.Send(data = 'hogehoge', sequence = 12, id = 1000, hostname = '4no.jp')
print req
res = requests.tx.ClientReader(str(req), hostname='4no.jp')
pprint(res.params)

req = requests.tx.Ok(count = 100, sequence = 43)
print req
res = requests.tx.ServerReader(str(req))
pprint(res.params)

req = requests.tx.Error(error = 900)
print req
res = requests.tx.ServerReader(str(req))
pprint(res.params)

req = requests.rx.Polling(padding = 10, hostname = '4no.jp')
print req
res = requests.rx.ClientReader(str(req), hostname='4no.jp')
pprint(res.params)

req = requests.rx.Receive(padding = 70, sequence = 43, id = 101, hostname = '4no.jp')
print req
res = requests.rx.ClientReader(str(req), hostname='4no.jp')
pprint(res.params)

req = requests.rx.Send(data = 'hogehoge', count = 12, id = 1000)
print req
res = requests.rx.ServerReader(str(req))
pprint(res.params)

req = requests.rx.Error(error = 900)
print req
res = requests.rx.ServerReader(str(req))
pprint(res.params)

