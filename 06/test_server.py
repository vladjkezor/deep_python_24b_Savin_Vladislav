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
        call = unittest.mock.call(f"Failed to fetch {url}")
        expected = '404 Error'.encode()

        self.assertEqual(result, expected)
        self.assertEqual(mock_print.call_args, call)


if __name__ == '__main__':
    unittest.main()
