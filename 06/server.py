import threading
import queue
import socket
import requests
import json
from collections import Counter


class Worker(threading.Thread):

    def __init__(self, que, top_k, server):
        super().__init__()
        self.que = que
        self.top_k = top_k
        self.server = server

    def run(self):
        while True:
            connection = self.que.get()
            if connection is None:
                self.que.put(None)
                break
            try:
                url = connection.recv(1024).decode()
                connection.sendall(self.fetch_and_process_url(url))
            except Exception as e:
                print(f"error {e}")
            finally:
                connection.close()
                with self.server.lock:
                    self.server.n_processed += 1
                    print(f'processed {self.server.n_processed} urls')

    def fetch_and_process_url(self, url):
        try:
            data = requests.get(url).text.split()
            top_words = dict(Counter(data).most_common(self.top_k))
            return json.dumps(top_words).encode()

        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return f'{e}'.encode()


class Server:

    def __init__(self, n_workers, top_k):
        self.top_k = top_k
        self.que = queue.Queue()
        self.n_processed = 0
        self.lock = threading.Lock()
        self.workers = [Worker(self.que, top_k, self) for _ in range(n_workers)]

        for worker in self.workers:
            worker.start()

    def start(self):
        print("start server")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("localhost", 20_000))
            sock.listen()
            try:
                while True:
                    client, addr = sock.accept()
                    self.que.put(client)
            except KeyboardInterrupt:
                print('Server closed')
                self.que.put(None)


serv = Server(3, 3)
serv.start()
