import time
import socket
import random

import threading


class Spammer:

    def __init__(self, spam_host, spam_port, proxy_host, proxy_port):
        self.spam_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.spam_client.bind((spam_host, spam_port))
        self.spam_client.connect((proxy_host, proxy_port))

    def spam(self):
        while True:
            # Make spam request - time to handle request (from 1s to 3s)
            request = str(random.randint(1, 3))
            self.spam_client.send(request.encode("utf-8"))
            time.sleep(0.3)

    def run(self):
        threading.Thread(target=self.spam).start()
