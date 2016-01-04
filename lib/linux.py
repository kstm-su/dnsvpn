import struct

_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2
_IOC_NRMASK = (1 << _IOC_NRBITS) - 1
_IOC_TYPEMASK = (1 << _IOC_TYPEBITS) - 1
_IOC_SIZEMASK = (1 << _IOC_SIZEBITS) - 1
_IOC_DIRMASK = (1 << _IOC_DIRBITS) - 1
_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS
_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2


def sizeof(t):
    fmt = '@'
    if t == 'int':
        fmt += 'i'
    elif t == 'unsigned int':
        fmt += 'I'
    elif t == 'struct sock_fprog':
        return sizeof('H') + (16+8+8+32 >> 3)
    else:
        fmt += t
    return len(struct.pack(fmt, 0))


def _IOC(dir_, type_, nr, size):
    res = dir_ << _IOC_DIRSHIFT
    res |= ord(type_) << _IOC_TYPESHIFT
    res |= nr << _IOC_NRSHIFT
    res |= size << _IOC_SIZESHIFT
    return res


def _IOC_TYPECHECK(t):
    return sizeof(t)


def _IOW(type_, nr, size):
    return _IOC(_IOC_WRITE, type_, nr, _IOC_TYPECHECK(size))


def _IOR(type_, nr, size):
    return _IOC(_IOC_READ, type_, nr, _IOC_TYPECHECK(size))


def ifreq(**kwargs):
    IFNAMSIZ = 16
    name = ''
    flags = 0
    if 'name' in kwargs:
        name = kwargs['name']
    if 'flags' in kwargs:
        flags = kwargs['flags']
    return struct.pack('%usH' % IFNAMSIZ, name, flags)


TUN_READQ_SIZE = 500
TUN_TUN_DEV = 0x0001
TUN_TAP_DEV = 0x0002
TUN_TYPE_MASK = 0x000f
TUN_FASYNC = 0x0010
TUN_NOCHECKSUM = 0x0020
TUN_NO_PI = 0x0040
TUN_ONE_QUEUE = 0x0080
TUN_PERSIST = 0x0100
TUN_VNET_HDR = 0x0200
TUN_TAP_MQ = 0x0400
TUNSETNOCSUM = _IOW('T', 200, 'int')
TUNSETDEBUG = _IOW('T', 201, 'int')
TUNSETIFF = _IOW('T', 202, 'int')
TUNSETPERSIST = _IOW('T', 203, 'int')
TUNSETOWNER = _IOW('T', 204, 'int')
TUNSETLINK = _IOW('T', 205, 'int')
TUNSETGROUP = _IOW('T', 206, 'int')
TUNGETFEATURES = _IOR('T', 207, 'unsigned int')
TUNSETOFFLOAD = _IOW('T', 208, 'unsigned int')
TUNSETTXFILTER = _IOW('T', 209, 'unsigned int')
TUNGETIFF = _IOR('T', 210, 'unsigned int')
TUNGETSNDBUF = _IOR('T', 211, 'int')
TUNSETSNDBUF = _IOW('T', 212, 'int')
TUNATTACHFILTER = _IOW('T', 213, 'struct sock_fprog')
TUNDETACHFILTER = _IOW('T', 214, 'struct sock_fprog')
TUNGETVNETHDRSZ = _IOR('T', 215, 'int')
TUNSETVNETHDRSZ = _IOW('T', 216, 'int')
TUNSETQUEUE = _IOW('T', 217, 'int')
TUNSETIFINDEX = _IOW('T', 218, 'unsigned int')
TUNGETFILTER = _IOR('T', 219, 'struct sock_fprog')
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000
IFF_ONE_QUEUE = 0x2000
IFF_VNET_HDR = 0x4000
IFF_TUN_EXCL = 0x8000
IFF_MULTI_QUEUE = 0x0100
IFF_ATTACH_QUEUE = 0x0200
IFF_DETACH_QUEUE = 0x0400
IFF_PERSIST = 0x0800
IFF_NOFILTER = 0x1000
TUN_TX_TIMESTAMP = 1
TUN_F_CSUM = 0x01
TUN_F_TSO4 = 0x02
TUN_F_TSO6 = 0x04
TUN_F_TSO_ECN = 0x08
TUN_F_UFO = 0x10
