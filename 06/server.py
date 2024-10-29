import threading
import queue
import socket
import requests
import json
from collections import Counter

URL = "http://ru.wikipedia.org/wiki/Python"
URLS = [URL] * 500
N_THREADS = 30
WORK_SIZE = len(URLS) // N_THREADS


class Worker(threading.Thread):

    def __init__(self, que, top_k):
        super().__init__()
        self.que = que
        self.top_k = top_k
        self.count = 0

    def fetch_url(self, url):
        data = requests.get(url).text.split()
        return dict(Counter(data).most_common(self.top_k))

    def run(self):
        while True:
            url = self.que.get()
            if url is None:
                self.que.put(url)
                break
            self.fetch_url(url)


class Server:

    def __init__(self, n_workers, top_k, urls):
        self.top_k = top_k

        self.que = queue.Queue()
        for url in urls:
            self.que.put(url)
        self.que.put(None)

        self.workers = [Worker(self.que, self.top_k) for _ in range(n_workers)]

    def start(self):
        for worker in self.workers:
            worker.start()
        for worker in self.workers:
            worker.join()


a = Server(N_THREADS, 4, URLS)
a.start()
