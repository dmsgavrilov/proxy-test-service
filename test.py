import time

from spammer import Spammer
from worker import Worker
from proxy_server import ProxyServer
import config

print("Running test script")

server = ProxyServer(config.spam_host, config.spam_port, config.proxy_host, config.proxy_port)
server.run()
print("server is running")

workers = [Worker(config.proxy_host, config.proxy_port) for _ in range(config.workers_num)]
for w in workers:
    w.run()
print("workers are running")

spam_client = Spammer(config.spam_host, config.spam_port, config.proxy_host, config.proxy_port)
spam_client.run()
print("spam client is running")

time.sleep(100)

workers[-1].close()
print(f"worker{len(workers)} is closed")

time.sleep(100)

workers[-1].open()
print(f"worker{len(workers)} is opened")

time.sleep(100)

print("test finished")
