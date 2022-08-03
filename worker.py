import time
import datetime

import socket
import threading
import queue

import logging

logging.basicConfig(filename=f"logs/{datetime.datetime.now()}.log", level=logging.INFO)


class Worker:
    counter = 0

    def __init__(self, proxy_host, proxy_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((proxy_host, proxy_port))

        # It's better to be done as separated server,
        # but here it is made as part of client
        # (will be changed in future with normal queue)
        self.work_queue = queue.LifoQueue()

        Worker.counter += 1
        self.work_num = self.counter

        self.lock = threading.Lock()
        self.closed = False

    def receive(self):
        while True:
            # Receive message from server
            data = self.client.recv(1024)

            message = data.decode("utf-8")
            if message == "QUEUE_SIZE":
                self.client.send(str(self.work_queue.qsize()).encode("utf-8"))
            else:
                self.work_queue.put(int(message))

    # This method will be improved in future
    def handle(self):
        while True:
            self.lock.acquire()
            closed = self.closed
            self.lock.release()
            if closed:
                time.sleep(5)
                continue
            if self.work_queue.empty():
                time.sleep(1)
                continue
            request = self.work_queue.get()
            time.sleep(request)

    def write_logs(self):
        while True:
            self.lock.acquire()
            closed = self.closed
            self.lock.release()
            if closed:
                time.sleep(5)
                continue
            time.sleep(10)
            logging.info(f"{datetime.datetime.now()}, worker{self.work_num} has {self.work_queue.qsize()} elements")

    def close(self):
        self.lock.acquire()
        self.closed = True
        self.lock.release()

    def open(self):
        self.lock.acquire()
        self.closed = False
        self.lock.release()

    def run(self):
        threading.Thread(target=self.receive).start()
        threading.Thread(target=self.handle).start()
        threading.Thread(target=self.write_logs).start()
