import socket

URL = "http://ru.wikipedia.org/wiki/Python"
URLS = [URL] * 20

for i in range(20):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('localhost', 20_000))
        client.sendall(URL.encode())

