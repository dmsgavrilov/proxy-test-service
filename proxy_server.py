import socket
import threading
import time


class ProxyServer:

    def __init__(self, spam_host, spam_port, proxy_host, proxy_port):
        self.spammer = (spam_host, spam_port)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((proxy_host, proxy_port))
        self.server.listen()

        self.workers = []

    def receive(self):
        while True:
            # Accept connection
            conn, address = self.server.accept()
            print("Connected with {}".format(str(address)))

            # Start handling thread for connection
            if address == self.spammer:
                thread = threading.Thread(target=self.proxy_spam_requests, args=(conn,))
                thread.start()
            else:
                self.workers.append(conn)

    def proxy_spam_requests(self, conn):
        while True:
            if not self.workers:
                time.sleep(3)
                continue
            spam = conn.recv(1024)
            self.least_load_worker().send(spam)

    def least_load_worker(self):
        loads = [0 for _ in range(len(self.workers))]
        for i in range(len(self.workers)):
            self.workers[i].send("QUEUE_SIZE".encode("utf-8"))
            loads[i] = int(self.workers[i].recv(1024).decode("utf-8"))
        return self.workers[loads.index(min(loads))]

    def run(self):
        threading.Thread(target=self.receive).start()
