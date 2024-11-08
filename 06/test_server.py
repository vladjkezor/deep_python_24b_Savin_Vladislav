import json
import unittest
from unittest.mock import patch, MagicMock
from server import Worker, Server
import requests


class TestServer(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_and_process_url(self, mock_get):
        mock_get.return_value.text = ('<html><body><p> Python fetch url </p>'
                                      '<p> test python fetch and process url '
                                      'python again</p></body></html>')

        url = 'test_url.com'
        server = MagicMock()
        que = MagicMock()
        top_k = 3
        test_worker = Worker(que, top_k, server)

        result = test_worker.fetch_and_process_url(url)
        expected = json.dumps({'python': 3, 'fetch': 2, 'url': 2}).encode()
        self.assertEqual(result, expected)

        top_k = 0
        test_worker = Worker(que, top_k, server)

        result = test_worker.fetch_and_process_url(url)
        expected = json.dumps({}).encode()
        self.assertEqual(result, expected)

        # top_k больше чем количество уникальных слов
        top_k = 100
        test_worker = Worker(que, top_k, server)

        result = test_worker.fetch_and_process_url(url)
        expected = json.dumps({"python": 3, "fetch": 2, "url": 2, "test": 1,
                               "and": 1, "process": 1, "again": 1}).encode()
        self.assertEqual(result, expected)

    @patch('requests.get')
    @patch('builtins.print')
    def test_fetch_and_process_error(self, mock_print, mock_get):
        mock_get.side_effect = requests.RequestException('404 Error')

        url = 'test_url.com'
        server = MagicMock()
        que = MagicMock()
        top_k = 3
        test_worker = Worker(que, top_k, server)

        result = test_worker.fetch_and_process_url(url)
        expected = '404 Error'.encode()
        call = unittest.mock.call(f"Failed to fetch {url}")

        self.assertEqual(result, expected)
        self.assertEqual(mock_print.call_args, call)

    @patch('server.Worker.fetch_and_process_url')
    @patch('builtins.print')
    def test_count_processed_urls(self, mock_print, mock_fetch):
        mock_fetch.return_value = 'mock'
        server = MagicMock()
        server.n_processed = 0

        mock_connection = MagicMock()
        mock_connection.recv.return_value = "mock.com".encode()
        que = MagicMock()
        que.get.side_effect = [mock_connection, None]

        test_worker = Worker(que, 2, server)
        test_worker.run()
        self.assertEqual(server.n_processed, 1)

        call = unittest.mock.call('processed 1 urls')
        self.assertEqual(mock_print.call_args, call)

    @patch('builtins.print')
    @patch('server.Worker.fetch_and_process_url')
    def test_worker_connection_sending_and_closing(self, mock_fetch, _):
        mock_fetch.side_effect = [b'{"word":1}', b'', b'404 Error']
        server = MagicMock()
        mock_connection = MagicMock()
        mock_connection.recv.return_value = "mock.com".encode()
        que = MagicMock()
        que.get.side_effect = [mock_connection, mock_connection,
                               mock_connection, None]

        test_worker = Worker(que, 2, server)
        test_worker.run()
        calls = [unittest.mock.call(b'{"word":1}'),
                 unittest.mock.call(b''),
                 unittest.mock.call(b'404 Error')]

        self.assertEqual(mock_connection.sendall.mock_calls, calls)
        self.assertEqual(mock_connection.sendall.call_count, 3)
        self.assertEqual(mock_connection.close.call_count, 3)

    @patch('builtins.print')
    def test_worker_connection_error(self, mock_print):
        server = MagicMock()
        server.n_processed = 0

        mock_connection = MagicMock()
        mock_connection.recv.side_effect = Exception('Connection error')
        que = MagicMock()
        que.get.side_effect = [mock_connection, None]

        test_worker = Worker(que, 2, server)
        test_worker.run()

        calls = [unittest.mock.call('Error: Connection error'),
                 unittest.mock.call('processed 1 urls')]

        self.assertEqual(mock_print.mock_calls, calls)
        self.assertEqual(mock_connection.close.call_count, 1)

    @patch('server.Worker')
    def test_server_init(self, MockWorker):  # pylint: disable=C0103
        n_workers = 4
        top_k = 3
        server = Server(n_workers, top_k)

        self.assertEqual(len(server.workers), 4)

        calls = [unittest.mock.call(server.que, top_k, server)
                 for _ in range(n_workers)]
        self.assertEqual(MockWorker.call_args_list, calls)

    @patch('server.Worker')
    @patch('socket.socket')
    def test_start_server(self, mock_sock, _):
        # Заглушка контекстного менеджера
        mock_sock_instance = mock_sock.return_value.__enter__.return_value
        mock_client = MagicMock()

        mock_sock_instance.accept.side_effect = [(mock_client, 'mock_address'),
                                                 KeyboardInterrupt()]

        server = Server(2, 2)
        server.que = MagicMock()
        server.start()

        calls = [unittest.mock.call(mock_client),
                 unittest.mock.call(None)]
        self.assertEqual(server.que.put.call_args_list, calls)


if __name__ == '__main__':
    unittest.main()
