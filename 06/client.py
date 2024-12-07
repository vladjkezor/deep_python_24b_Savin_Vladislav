import threading
import queue
import socket
import argparse


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
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(('localhost', 12345))
                    sock.sendall(url.encode())
                    data = sock.recv(1024).decode()
                    print(f'{url} {data}')
            except Exception as e:
                print(f"Client error: {e}")


class Client:
    def __init__(self, n_workers, filename):
        self.que = queue.Queue(maxsize=20)
        self.filename = filename
        self.workers = [ClientWorker(self.que) for _ in range(n_workers)]

    def start(self):
        for worker in self.workers:
            worker.start()

        with open(self.filename, 'r', encoding='utf-8') as urls:
            for url in urls:
                self.que.put(url.strip())
        self.que.put(None)

        for worker in self.workers:
            worker.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', default=5, type=int)
    parser.add_argument('--filename', default='urls.txt', type=str)

    args = parser.parse_args()

    client = Client(args.workers, args.filename)
    client.start()
