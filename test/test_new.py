import errno
from http import client
import io
import itertools
import os
import array
import re
import socket
import time
import threading
import warnings

import unittest

TestCase = unittest.TestCase

from test import support
from test.support import socket_helper

HOST = socket_helper.HOST

class SleepySocket(socket.socket):
    def __init__(self, sleep, *args, **kwargs):
        self.sleep = sleep
        super(SleepySocket, self).__init__(*args, **kwargs)
        
    def create_connection(self, *args, **kwargs) -> None:
        """
        Accepts a connection to the socket, but sleeps `self.sleep`
        seconds before doing so.
        """
        time.sleep(self.sleep)
        super(SleepySocket, self).create_connection(*args, **kwargs)

class NewTimeoutTests(TestCase):
    PORT = None

    def setUp(self):
        self.serv = SleepySocket(sleep=200, family=socket.AF_INET, type=socket.SOCK_STREAM)
        NewTimeoutTests.PORT = socket_helper.bind_port(self.serv)
        self.serv.listen()

    def tearDown(self):
        self.serv.close()
        self.serv = None

    def test_negative_timeout_raises(self):
        with self.assertRaises(ValueError):
            http_conn = client.HTTPConnection(
                HOST, NewTimeoutTests.PORT, timeout=-1
            )
            http_conn.connect()

    def test_timeout_expires(self):
        with self.assertRaises(BlockingIOError):
            http_conn = client.HTTPConnection(
                HOST, NewTimeoutTests.PORT, timeout=0
            )
            http_conn.connect()

