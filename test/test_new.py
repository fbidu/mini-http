import errno
from http import client
import io
import itertools
import os
import array
import re
import socket
import threading
import warnings

import unittest

TestCase = unittest.TestCase

from test import support
from test.support import socket_helper

HOST = socket_helper.HOST


class TimeoutBoundariesTest(TestCase):
    PORT = None

    def setUp(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TimeoutBoundariesTest.PORT = socket_helper.bind_port(self.serv)
        self.serv.listen()

    def tearDown(self):
        self.serv.close()
        self.serv = None

    def test_negative_timeout_raises(self):
        with self.assertRaises(ValueError):
            http_conn = client.HTTPConnection(
                HOST, TimeoutBoundariesTest.PORT, timeout=-1
            )
            http_conn.connect()
