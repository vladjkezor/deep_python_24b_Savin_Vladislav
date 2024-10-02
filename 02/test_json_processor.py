import unittest
from unittest.mock import MagicMock
import json

from json_processor import process_json


class TestJsonProcessor(unittest.TestCase):
    def test_from_example(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]
        result = []

        def callback(key, token):
            result.append((key, token))

        process_json(json_str, required_keys, tokens, callback)
        self.assertEqual(result, [('key1', 'WORD1'), ('key1', 'word2')])

    def test_with_no_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        tokens = ["WORD1", "word2"]
        result = []
        expected_result = [('key1', 'WORD1'),
                           ('key1', 'word2'),
                           ('key2', 'word2')]

        def callback(key, token):
            result.append((key, token))

        process_json(json_str, tokens=tokens, callback=callback)
        self.assertEqual(result, expected_result)

    def test_with_no_tokens(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        callback = MagicMock()

        process_json(json_str, required_keys, callback=callback)
        self.assertFalse(callback.called)

    def test_token_case_sensitivity(self):
        json_str = '{"key1": "Word word2 WORD4 wORd3"}'
        required_keys = ['key1', 'key2']
        tokens = ['word', 'WORd2', 'woRD3']
        result = []

        def callback(key, token):
            result.append((key, token))

        expected_result = [("key1", 'word'),
                           ('key1', 'WORd2'),
                           ('key1', 'woRD3')]

        process_json(json_str, required_keys, tokens, callback)
        self.assertEqual(result, expected_result)

    def test_no_match_tokens(self):
        json_str = '{"key1": "Word word2 WORD4 wORd3"}'
        required_keys = ['key1', 'key2']
        tokens = ['key', 'json', 'processing']
        callback = MagicMock()
        process_json(json_str, required_keys, tokens, callback)
        self.assertFalse(callback.called)

    def test_no_match_keys(self):
        json_str = ('{"key1": "Word word2 WORD4 wORd3",'
                    ' "key2": "Json json",'
                    '"key3": "Json json"}')
        required_keys = ['wrong_key1', 'excellent_key2', 'Key3']
        tokens = ['Word', 'word2', 'WORD4', 'json']
        callback = MagicMock()
        process_json(json_str, required_keys, tokens, callback)
        self.assertFalse(callback.called)

    def test_full_str_token(self):
        json_str = '{"key1": "Word word2 WORD4 ", "key2": "Json test json"}'
        required_keys = ['key1', 'key2']
        tokens = ['Word word2 WORD4 ', "Json test"]
        result = []

        def callback(key, token):
            result.append((key, token))

        expected_result = [('key1', 'Word word2 WORD4 '),
                           ('key2', 'Json test')]
        process_json(json_str, required_keys, tokens, callback)
        self.assertEqual(expected_result, result)

    def test_empty_json(self):
        json_str = '{}'
        required_keys = ['key1', 'key2']
        tokens = ['word1 ', "word2"]
        callback = MagicMock()
        process_json(json_str, required_keys, tokens, callback)
        self.assertFalse(callback.called)

    def test_empty_values(self):
        json_str = '{"key1": "", "key2": ""}'
        required_keys = ["key1", "key2"]
        tokens = ["word1", "word2"]
        callback = MagicMock()
        process_json(json_str, required_keys, tokens, callback)
        self.assertFalse(callback.called)

    def test_invalid_json(self):
        json_str = '{"key1": "word1 word2"'  # неправильный формат

        with self.assertRaises(json.JSONDecodeError):
            process_json(json_str, ["key1"], ["word1"], None)


if __name__ == '__main__':
    unittest.main()
