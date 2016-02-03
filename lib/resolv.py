import re


def get_resolv_conf():
    res = {
        'nameserver': [],
        'domain': [],
        'search': [],
        'sortlist': [],
        'options': [],
    }
    for line in open('/etc/resolv.conf'):
        match = re.search(
            r'(nameserver|domain|search|sortlist|options)\s+(.*)$',
            line
        )
        if match is None:
            continue
        res[match.group(1)].append(match.group(2))
    return res
