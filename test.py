#!/usr/bin/env python3

import unittest
import random

from lib import query


class QueryTestCase(unittest.TestCase):
    count = 1000

    def query_equal(self, Query, ep=None, dp=None):
        if ep is None:
            ep = {}
        if dp is None:
            dp = {}
        for i in range(self.count):
            params = {k: v() for k, v in ep.items()}
            e = Query(**params)
            d = Query(e, **dp)
            self.assertEqual(d.decode(), params, (str(e), e.pattern(**dp)))

    def query_not_equal(self, Query, ep=None, dp=None):
        if ep is None:
            ep = {}
        if dp is None:
            dp = {}
        for i in range(self.count):
            params = {k: v() for k, v in ep.items()}
            e = Query(**params)
            d = Query(e, **dp)
            self.assertNotEqual(d.decode(), params, (str(e), e.pattern(**dp)))

    def test_ok(self):
        self.query_equal(query.Ok, {
            'count': lambda: random.randint(1, 0xffff),
            'sequence': lambda: random.randint(0, 0xffff),
        })
        self.query_not_equal(query.Ok, {
            'count': lambda: 0,
            'sequence': lambda: random.randint(0, 0xffff),
        })

    def test_error(self):
        self.query_equal(query.Error, {
            'error': lambda: random.randint(0, 0xffff),
        })

    def test_polling(self):
        hostname = '.'.join([str(random.randint(0, 0xff)) for i in range(3)])
        self.query_equal(query.Polling, {
            'hostname': lambda: hostname,
            'padding': lambda: random.randint(1, 0xff),
        }, {
            'hostname': hostname,
        })

    def test_rx_initialize(self):
        self.query_equal(query.RxInitialize, {
            'count': lambda: random.randint(1, 0xffff),
            'id': lambda: random.randint(0, 0xffff),
            'data': lambda: str(random.randint(0, 0xffffffff)),
        })

    def test_rx_send(self):
        self.query_equal(query.RxSend, {
            'sequence': lambda: random.randint(0, 0xffff),
            'id': lambda: random.randint(0, 0xffff),
            'data': lambda: str(random.randint(0, 0xffffffff)),
        })

    def test_rx_receive(self):
        hostname = '.'.join([str(random.randint(0, 0xff)) for i in range(3)])
        self.query_equal(query.Receive, {
            'padding': lambda: random.randint(1, 0xff),
            'id': lambda: random.randint(0, 0xffff),
            'sequence': lambda: random.randint(0, 0xffff),
            'hostname': lambda: hostname,
        }, {
            'hostname': hostname,
        })

    def test_tx_initialize(self):
        hostname = '.'.join([str(random.randint(0, 0xff)) for i in range(3)])
        self.query_equal(query.TxInitialize, {
            'count': lambda: random.randint(1, 0xffff),
            'id': lambda: random.randint(0, 0xffff),
            'hostname': lambda: hostname,
        }, {
            'hostname': hostname,
        })

    def test_tx_send(self):
        hostname = '.'.join([str(random.randint(0, 0xff)) for i in range(3)])
        self.query_equal(query.TxSend, {
            'sequence': lambda: random.randint(0, 0xffff),
            'id': lambda: random.randint(0, 0xffff),
            'data': lambda: str(random.randint(0, 0xffffffff)),
            'hostname': lambda: hostname,
        }, {
            'hostname': hostname,
        })


if __name__ == '__main__':
    unittest.main()
