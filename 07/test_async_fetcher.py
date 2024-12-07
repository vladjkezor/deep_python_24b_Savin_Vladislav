import asyncio
import unittest
from unittest import mock
from unittest.mock import AsyncMock, patch

from async_fetcher import read_urls, fetch_url, worker, fetch_batch_urls


class TestAsyncFetcher(unittest.IsolatedAsyncioTestCase):
    @patch('asyncio.Queue.put')
    async def test_read_urls(self, que_put):
        filename = 'test_urls.txt'
        que = asyncio.Queue()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('test1.com\n')
            f.write('test2.com\n')

        expected = [
            unittest.mock.call('test1.com'),
            unittest.mock.call('test2.com'),
            unittest.mock.call(None)
        ]

        await read_urls(filename, que)
        self.assertEqual(expected, que_put.mock_calls)

    @patch('asyncio.Queue.put')
    async def test_read_urls_empty_file(self, que_put):
        filename = 'empty_urls.txt'
        que = asyncio.Queue()
        with open(filename, 'w', encoding='utf-8') as _:
            pass

        expected = [unittest.mock.call(None)]
        await read_urls(filename, que)
        self.assertEqual(expected, que_put.mock_calls)

    @patch('builtins.print')
    @patch('aiohttp.ClientSession')
    async def test_fetch_url_success(self, mock_session, mock_print):
        mock_text = AsyncMock(
            return_value='<html><body><p> Python fetch url </p>'
                         '<p> test python fetch and process url '
                         'python again</p></body></html>'
        )
        mock_response = AsyncMock(text=mock_text)
        mock_session.get.return_value.__aenter__.return_value = mock_response

        await fetch_url('test_url', mock_session)
        expected = ("test_url, {'python': 3, 'fetch': 2,"
                    " 'url': 2, 'test': 1, 'and': 1}")
        mock_print.assert_called_with(expected)

        expected_calls = [
            mock.call('test_url'),
            mock.call().__aenter__(),  # pylint: disable=C2801
            mock.call().__aenter__().text(),  # pylint: disable=C2801
            mock.call().__aexit__(None, None, None),
        ]
        self.assertEqual(expected_calls, mock_session.get.mock_calls)

    @patch('builtins.print')
    @patch('aiohttp.ClientSession')
    async def test_fetch_url_error(self, mock_session, mock_print):
        mock_session.get.side_effect = Exception('403 Error')

        await fetch_url('test_url', mock_session)
        expected = 'Failed to fetch test_url, error: 403 Error'
        mock_print.assert_called_with(expected)

        expected_call = [mock.call('test_url')]
        self.assertEqual(expected_call, mock_session.get.mock_calls)

    @patch('builtins.print')
    @patch('aiohttp.ClientSession')
    async def test_fetch_url_timeout(self, mock_session, mock_print):
        mock_session.get.side_effect = asyncio.TimeoutError

        await fetch_url('test_url', mock_session)
        expected = 'Timeout while fetching test_url'
        mock_print.assert_called_with(expected)

        expected_call = [mock.call('test_url')]
        self.assertEqual(expected_call, mock_session.get.mock_calls)

    @patch('async_fetcher.fetch_url')
    async def test_worker(self, mock_fetch):
        mock_que = AsyncMock()
        mock_que.get.side_effect = ['url1', 'url2', None]
        mock_session = AsyncMock()

        await worker(mock_que, mock_session)
        expected_calls = [mock.call('url1', mock_session),
                          mock.call('url2', mock_session)]
        self.assertEqual(mock_fetch.mock_calls, expected_calls)

    @patch('async_fetcher.fetch_url')
    async def test_worker_empty_que(self, mock_fetch):
        mock_que = AsyncMock()
        mock_que.get.side_effect = [None]
        mock_session = AsyncMock()

        await worker(mock_que, mock_session)
        expected_calls = []
        self.assertEqual(mock_fetch.mock_calls, expected_calls)

    @patch('aiohttp.ClientSession.get')
    def test_fetch_batch_urls_multiple_workers_and_urls(self, mock_session):
        filename = 'test_urls.txt'
        n_workers = 3

        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(5):
                f.write(f'test{i}.com\n')

        mock_resp = AsyncMock()
        mock_session.return_value.__aenter__.return_value = mock_resp

        mock_resp.text = AsyncMock(side_effect=[
            f"result {i}" for i in range(5)
        ])

        with patch('builtins.print') as mock_print:
            asyncio.run(fetch_batch_urls(n_workers, filename))
            expected__print_res = [
                unittest.mock.call("test0.com, {'result': 1, '0': 1}"),
                unittest.mock.call("test1.com, {'result': 1, '1': 1}"),
                unittest.mock.call("test2.com, {'result': 1, '2': 1}"),
                unittest.mock.call("test3.com, {'result': 1, '3': 1}"),
                unittest.mock.call("test4.com, {'result': 1, '4': 1}"),
            ]
            self.assertEqual(mock_print.mock_calls, expected__print_res)

    @patch('aiohttp.ClientSession.get')
    def test_fetch_batch_urls_one_worker(self, mock_session):
        filename = 'test_urls.txt'
        n_workers = 1
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(3):
                f.write(f'test{i}.com\n')

        mock_resp = AsyncMock()
        mock_session.return_value.__aenter__.return_value = mock_resp
        mock_resp.text = AsyncMock(side_effect=[
            f"result {i}" for i in range(3)
        ])

        with patch('builtins.print') as mock_print:
            asyncio.run(fetch_batch_urls(n_workers, filename))
            expected__print_res = [
                unittest.mock.call("test0.com, {'result': 1, '0': 1}"),
                unittest.mock.call("test1.com, {'result': 1, '1': 1}"),
                unittest.mock.call("test2.com, {'result': 1, '2': 1}")
            ]
            self.assertEqual(mock_print.mock_calls, expected__print_res)

    @patch('aiohttp.ClientSession.get')
    def test_fetch_batch_urls_no_workers(self, mock_session):
        filename = 'test_urls.txt'
        n_workers = 0
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(3):
                f.write(f'test{i}.com\n')

        mock_resp = AsyncMock()
        mock_session.return_value.__aenter__.return_value = mock_resp
        mock_resp.text = AsyncMock(side_effect=[
            f"result {i}" for i in range(3)
        ])

        with patch('builtins.print') as mock_print:
            asyncio.run(fetch_batch_urls(n_workers, filename))
            expected__print_res = []
            self.assertEqual(mock_print.mock_calls, expected__print_res)

    @patch('aiohttp.ClientSession.get')
    def test_fetch_batch_urls_no_urls(self, mock_session):
        filename = 'empty_urls.txt'
        n_workers = 3
        with open(filename, 'w', encoding='utf-8'):
            pass

        mock_resp = AsyncMock()
        mock_session.return_value.__aenter__.return_value = mock_resp

        with patch('builtins.print') as mock_print:
            asyncio.run(fetch_batch_urls(n_workers, filename))
            expected__print_res = []
            self.assertEqual(mock_print.mock_calls, expected__print_res)


if __name__ == '__main__':
    unittest.main()
