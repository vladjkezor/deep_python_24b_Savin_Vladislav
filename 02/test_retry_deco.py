import unittest
from unittest import mock
from unittest.mock import patch

from retry_deco import retry_deco


class TestRetryDecorator(unittest.TestCase):

    @patch('builtins.print')
    def test_first_attempt_success(self, mock_print):
        @retry_deco(3)
        def add(a, b):
            return a + b

        add(2, 3)

        expected_print = mock.call('run "add", ',
                                   'positional args = (2, 3), ',
                                   '', 'attempt=1, result=5', sep='')

        self.assertEqual(mock_print.call_args, expected_print)
        self.assertEqual(mock_print.call_count, 1)

    @patch('builtins.print')
    def test_expected_error(self, mock_print):

        @retry_deco(2, [ValueError])
        def check_int(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, int)

        check_int(value=1)
        expected_print = mock.call('run "check_int", ',
                                   '', "keyword kwargs = {'value': 1}, ",
                                   'attempt=1, result=True', sep='')

        self.assertEqual(mock_print.call_args, expected_print)
        self.assertEqual(mock_print.call_count, 1)

        mock_print.reset_mock()
        check_int(value=None)

        expected_print = mock.call('run "check_int", ', '',
                                   "keyword kwargs = {'value': None}, ",
                                   'attempt=1, exception = ValueError', sep='')

        self.assertEqual(mock_print.call_args, expected_print)
        self.assertEqual(mock_print.call_count, 1)

    @patch('builtins.print')
    def test_count_of_retries(self, mock_print):

        @retry_deco(3)
        def check_str(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, str)

        calls = [mock.call('run "check_str", ', '',
                           "keyword kwargs = {'value': None}, ",
                           'attempt=1, exception = ValueError', sep=''),
                 mock.call('run "check_str", ', '',
                           "keyword kwargs = {'value': None}, ",
                           'attempt=2, exception = ValueError', sep=''),
                 mock.call('run "check_str", ', '',
                           "keyword kwargs = {'value': None}, ",
                           'attempt=3, exception = ValueError', sep='')]

        check_str(value=None)

        self.assertEqual(mock_print.call_args_list, calls)
        self.assertEqual(mock_print.call_count, 3)
