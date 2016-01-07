from threading import Thread
from queue import Queue


class Connection(Thread):
    daemon = True

    def __init__(self, pool):
        Thread.__init__(self)
        self.pool = pool

    def run(self):
        self.thread()
        self.end()

    def end(self):
        del self.pool[self.ident]
        self.pool.next()

    def thread(self):
        return


class ConnectionPool(dict):
    max = 20

    def __init__(self, Conn):
        dict.__init__(self)
        self.queue = Queue()
        self.Conn = Conn

    def push(self, params=None):
        conn = self.Conn(self)
        conn.params = params
        self.queue.put(conn)
        if len(self) < self.max:
            self.next()

    def next(self):
        if self.queue.empty():
            return
        conn = self.queue.get()
        conn.start()
        self[conn.ident] = conn
