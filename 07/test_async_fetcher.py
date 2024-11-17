import unittest
from unittest import mock
from unittest.mock import AsyncMock, patch

from async_fetcher import read_urls, fetch_url, worker, fetch_batch_urls


class TestAsyncFetcher(unittest.IsolatedAsyncioTestCase):
    def test_read_urls(self):
        filename = 'test_urls.txt'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('test1.com\n')
            f.write('test2.com\n')

        expected = ['test1.com', 'test2.com']
        self.assertEqual(expected, read_urls(filename))

    def test_read_urls_empty_file(self):
        filename = 'empty_urls.txt'
        with open(filename, 'w', encoding='utf-8') as _:
            pass

        expected = []
        self.assertEqual(expected, read_urls(filename))

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

    @patch('async_fetcher.worker')
    @patch('asyncio.Queue.put')
    @patch('async_fetcher.read_urls')
    async def test_fetch_batch_(self, mock_read, mock_put, mock_worker):
        mock_read.return_value = ['url1', 'url2', 'url3']
        filename = 'test_filename'
        n_workers = 5

        await fetch_batch_urls(n_workers, filename)

        mock_read.assert_called_once_with(filename)

        expected_que_calls = [mock.call('url1'),
                              mock.call('url2'),
                              mock.call('url3'),
                              mock.call(None)]
        self.assertEqual(mock_put.mock_calls, expected_que_calls)

        self.assertEqual(mock_worker.call_count, n_workers)

    @patch('async_fetcher.worker')
    @patch('async_fetcher.read_urls')
    async def test_fetch_batch_zero_workers(self, mock_read, mock_worker):
        mock_read.return_value = ['url1', 'url2', 'url3']
        filename = 'test_filename'
        n_workers = 0
        await fetch_batch_urls(n_workers, filename)
        mock_worker.assert_not_called()
