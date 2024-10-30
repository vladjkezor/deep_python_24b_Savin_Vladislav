import threading
import queue
import socket
import requests
import json
from collections import Counter


class Worker(threading.Thread):

    def __init__(self, que, top_k):
        super().__init__()
        self.que = que
        self.top_k = top_k

    def run(self):
        while True:
            connection = self.que.get()
            url = connection.recv(1024).decode()
            data = requests.get(url).text.split()
            print(f'{self.name} --- {Counter(data).most_common(self.top_k)}')
            connection.close()


class Server:

    def __init__(self, n_workers, top_k):
        self.top_k = top_k
        self.que = queue.Queue()
        self.workers = [Worker(self.que, top_k) for _ in range(n_workers)]

        for worker in self.workers:
            worker.start()

    def start(self):
        print("start server")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("localhost", 20_000))
            sock.listen()

            while True:
                client, addr = sock.accept()
                self.que.put(client)


serv = Server(5, 3)
serv.start()
