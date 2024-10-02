import unittest

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

        process_json(json_str, None, tokens, callback)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
