import unittest
from unittest import mock
from unittest.mock import patch

from retry_deco import retry_deco


class TestRetryDecorator(unittest.TestCase):

    @patch('builtins.print')
    def test_first_attempt_success_with_args(self, mock_print):
        @retry_deco(3)
        def add(a, b):
            return a + b

        add(2, 3)

        calls = mock.call('run "add", ',
                          'positional args = (2, 3), ',
                          '', 'attempt=1, result=5', sep='')

        self.assertEqual(mock_print.call_args, calls)
        self.assertEqual(mock_print.call_count, 1)

    @patch('builtins.print')
    def test_first_attempt_success_with_kwargs(self, mock_print):
        @retry_deco(3)
        def add(a, b):
            return a + b

        add(a=10, b=23)

        calls = mock.call('run "add", ', '',
                          "keyword kwargs = {'a': 10, 'b': 23}, ",
                          'attempt=1, result=33', sep='')

        self.assertEqual(mock_print.call_args, calls)
        self.assertEqual(mock_print.call_count, 1)

    @patch('builtins.print')
    def test_first_attempt_success_full_args(self, mock_print):
        @retry_deco(3)
        def add(a, b, c, d):
            return a + b + c + d

        add(100, 5, c=7, d=15)

        calls = mock.call('run "add", ', 'positional args = (100, 5), ',
                          "keyword kwargs = {'c': 7, 'd': 15}, ",
                          'attempt=1, result=127', sep='')

        self.assertEqual(mock_print.call_args, calls)
        self.assertEqual(mock_print.call_count, 1)

    @patch('builtins.print')
    def test_expected_error(self, mock_print):

        @retry_deco(2, [ValueError])
        def check_int(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, int)

        check_int(value=1)
        calls = mock.call('run "check_int", ',
                          '', "keyword kwargs = {'value': 1}, ",
                          'attempt=1, result=True', sep='')

        self.assertEqual(mock_print.call_args, calls)
        self.assertEqual(mock_print.call_count, 1)

        mock_print.reset_mock()

        with self.assertRaises(ValueError):
            check_int(value=None)

        calls = mock.call('run "check_int", ', '',
                          "keyword kwargs = {'value': None}, ",
                          'attempt=1, Normal Exception = ValueError', sep='')

        self.assertEqual(mock_print.call_args, calls)
        self.assertEqual(mock_print.call_count, 1)

    @patch('builtins.print')
    def test_expected_error_from_list(self, mock_print):
        @retry_deco(2, [TypeError, ValueError, ZeroDivisionError])
        def division(value):
            if value is None:
                raise ValueError
            if not isinstance(value, int):
                raise TypeError()
            return 42 / value

        with self.assertRaises(ValueError):
            division(value=None)

        calls = mock.call('run "division", ', '',
                          "keyword kwargs = {'value': None}, ",
                          'attempt=1, Normal Exception = ValueError', sep='')

        self.assertEqual(mock_print.call_args, calls)
        self.assertEqual(mock_print.call_count, 1)

        mock_print.reset_mock()

        with self.assertRaises(TypeError):
            division('пятнадцать')

        calls = mock.call('run "division", ',
                          "positional args = ('пятнадцать',), ", '',
                          'attempt=1, Normal Exception = TypeError', sep='')

        self.assertEqual(mock_print.call_args, calls)
        self.assertEqual(mock_print.call_count, 1)

        mock_print.reset_mock()

        with self.assertRaises(ZeroDivisionError):
            division(0)

        calls = mock.call('run "division", ',
                          "positional args = (0,), ", '',
                          'attempt=1, Normal Exception = ZeroDivisionError',
                          sep='')

        self.assertEqual(mock_print.call_args, calls)
        self.assertEqual(mock_print.call_count, 1)

        mock_print.reset_mock()

    @patch('builtins.print')
    def test_multiple_retries(self, mock_print):

        @retry_deco(3)
        def check_str(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, str)

        calls = [mock.call('run "check_str", ', '',
                           "keyword kwargs = {'value': None}, ",
                           'attempt=1, Exception = ValueError', sep=''),
                 mock.call('run "check_str", ', '',
                           "keyword kwargs = {'value': None}, ",
                           'attempt=2, Exception = ValueError', sep=''),
                 mock.call('run "check_str", ', '',
                           "keyword kwargs = {'value': None}, ",
                           'attempt=3, Exception = ValueError', sep='')]
        with self.assertRaises(ValueError):
            check_str(value=None)

        self.assertEqual(mock_print.call_args_list, calls)
        self.assertEqual(mock_print.call_count, 3)

    @patch('builtins.print')
    def test_zero_retries(self, mock_print):

        @retry_deco(0)
        def check_str(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, str)

        calls = []

        check_str(value=None)

        self.assertEqual(mock_print.call_args_list, calls)
        self.assertEqual(mock_print.call_count, 0)

    @patch('builtins.print')
    def test_first_attempt_success_zero_args(self, mock_print):
        @retry_deco(3)
        def hello():
            return "Hello Python"

        hello()

        calls = mock.call('run "hello", ', '',
                          '', "attempt=1, result='Hello Python'", sep='')

        self.assertEqual(mock_print.call_args, calls)
        self.assertEqual(mock_print.call_count, 1)
