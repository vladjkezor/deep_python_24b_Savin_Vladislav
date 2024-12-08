import threading
import queue
import socket
import json
import re
import argparse
from collections import Counter
from bs4 import BeautifulSoup
import requests


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
                result = self.fetch_and_process_url(url)
                connection.sendall(result)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                connection.close()
                with self.server.lock:
                    self.server.n_processed += 1
                    print(f'processed {self.server.n_processed} urls')

    def fetch_and_process_url(self, url):
        try:
            response = requests.get(url, timeout=5)
        except requests.RequestException as e:
            with self.server.lock:
                print(f"Failed to fetch {url}")
            return f'{e}'.encode()
        # Обработка текста страницы
        text = BeautifulSoup(response.text, 'html.parser')
        words = re.findall(r'\b\w+\b', text.get_text().lower())

        top_words = dict(Counter(words).most_common(self.top_k))
        return json.dumps(top_words, ensure_ascii=False).encode()


class Server:

    def __init__(self, n_workers, top_k):
        self.top_k = top_k
        self.que = queue.Queue(maxsize=n_workers * 2)
        self.n_processed = 0
        self.lock = threading.Lock()
        self.workers = [Worker(self.que, top_k, self)
                        for _ in range(n_workers)]

    def start(self):
        print("Start server")
        for worker in self.workers:
            worker.start()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("localhost", 12345))
            sock.listen()

            try:
                while True:
                    client, _ = sock.accept()
                    self.que.put(client)
            except KeyboardInterrupt:
                print('Server closed')
                self.que.put(None)
            for worker in self.workers:
                worker.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--workers', default=5, type=int)
    parser.add_argument('-k', '--top_k', default=3, type=int)

    args = parser.parse_args()

    serv = Server(args.workers, args.top_k)
    serv.start()
