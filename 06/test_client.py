import unittest
from unittest.mock import patch, MagicMock

from client import Client, ClientWorker


class TestClient(unittest.TestCase):

    @patch('builtins.print')
    @patch('socket.socket')
    def test_worker(self, mock_sock, mock_print):
        que = MagicMock()
        que.get.side_effect = ['test.com', None]
        worker = ClientWorker(que)

        mock_sock_inst = mock_sock.return_value.__enter__.return_value
        mock_sock_inst.recv.return_value = b'{"word":1}'
        worker.run()

        connect_call = unittest.mock.call(('localhost', 12345))
        self.assertEqual(mock_sock_inst.connect.call_args, connect_call)
        send_call = unittest.mock.call(b'test.com')
        self.assertEqual(mock_sock_inst.sendall.call_args, send_call)

        print_call = unittest.mock.call('test.com {"word":1}')
        self.assertEqual(mock_print.call_args, print_call)

    @patch('builtins.print')
    @patch('socket.socket')
    def test_worker_error(self, mock_sock, mock_print):
        que = MagicMock()
        que.get.side_effect = ['test.com', None]
        worker = ClientWorker(que)

        mock_sock_inst = mock_sock.return_value.__enter__.return_value
        mock_sock_inst.connect.side_effect = Exception("Connection error")
        worker.run()

        print_call = unittest.mock.call('Client error: Connection error')
        self.assertEqual(mock_print.call_args, print_call)

    def test_client_url_reading(self):
        filename = 'test_urls.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('test1.com\n')
            f.write('test2.com\n')

        client = Client(2, filename)
        # В очереди должно быть 2 ссылки и None
        self.assertEqual(client.que.qsize(), 3)
        self.assertEqual(client.que.get_nowait(), 'test1.com')
        self.assertEqual(client.que.get_nowait(), 'test2.com')
        self.assertEqual(client.que.get_nowait(), None)

    @patch('client.ClientWorker')
    def test_client_starts_workers(self, mock_client_worker):
        filename = 'test_urls.txt'
        with open(filename, 'w', encoding='utf-8') as _:
            pass
        n_workers = 5
        client = Client(n_workers, filename)
        self.assertEqual(len(client.workers), n_workers)

        calls = [unittest.mock.call(client.que)
                 for _ in range(n_workers)]
        self.assertEqual(mock_client_worker.call_args_list, calls)

    def text_empty_urls(self):
        filename = 'test_empty_urls.txt'
        n_workers = 5
        with open(filename, 'w', encoding='utf-8') as _:
            pass

        client = Client(n_workers, filename)
        self.assertEqual(client.que.qsize(), 1)
        self.assertEqual(client.que.get_nowait(), None)


if __name__ == '__main__':
    unittest.main()
