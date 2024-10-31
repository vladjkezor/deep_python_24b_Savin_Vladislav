import threading
import queue
import socket

URL = "http://ru.wikipeia.org/"
URLS = [URL] * 10


class ClientWorker(threading.Thread):
    def __init__(self, que):
        super().__init__()
        self.que = que

    def run(self):
        while True:
            url = self.que.get()
            if url is None:
                self.que.put(None)
                break

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect(('localhost', 20_000))
                client.sendall(url.encode())

                data = client.recv(1024).decode()
                print(f' {url} {data}')


class Client:
    def __init__(self, urls, n_workers):
        self.que = queue.Queue()
        for url in urls:
            self.que.put(url)
        self.que.put(None)

        self.workers = [ClientWorker(self.que) for _ in range(n_workers)]
        for worker in self.workers:
            worker.start()


cl = Client(URLS, 40)
