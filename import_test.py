from lib.dns import requests

print requests
tx = requests.tx.Initialize(count = 1000, id = 1000, hostname = '4no.jp')
print str(tx)

