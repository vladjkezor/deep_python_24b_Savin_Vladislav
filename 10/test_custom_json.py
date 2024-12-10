import unittest
from custom_json import loads, dumps


class TestCustomJson(unittest.TestCase):
    def test_loads_valid_json(self):
        test_json = '{"key1": "value1", "key2": 123, "key3": 45.67}'
        expected = {"key1": "value1", "key2": 123, "key3": 45.67}
        self.assertEqual(loads(test_json), expected)

    def test_loads_invalid_json_format(self):
        with self.assertRaises(TypeError) as e:
            loads('"key1": "value1", "key2": 123')
        self.assertEqual(str(e.exception), 'Invalid JSON')

        with self.assertRaises(TypeError) as e:
            loads('{"key1": "value1", "key2": 123')
        self.assertEqual(str(e.exception), 'Invalid JSON')

        with self.assertRaises(TypeError) as e:
            loads('"key1": "value1", "key2": 123}')
        self.assertEqual(str(e.exception), 'Invalid JSON')

    def test_loads_invalid_key_format(self):
        with self.assertRaises(TypeError) as e:
            loads('{key1: "value1"}')
        self.assertEqual(str(e.exception), 'Invalid JSON key format')

        with self.assertRaises(TypeError) as e:
            loads("{'key2': 'value2'}")
        self.assertEqual(str(e.exception), 'Invalid JSON key format')

        with self.assertRaises(TypeError) as e:
            loads('{42: "value1"}')
        self.assertEqual(str(e.exception), 'Invalid JSON key format')

    def test_loads_unsupported_value(self):
        with self.assertRaises(TypeError) as e:
            loads('{"key1": [1, 2, 3]}')
        self.assertEqual(str(e.exception),
                         'Unsupported JSON value format')

        with self.assertRaises(TypeError) as e:
            loads('{"key1": {"key1": "value1"}}')
        self.assertEqual(str(e.exception),
                         'Unsupported JSON value format')

    def test_dumps_valid_dict(self):
        test_dict = {'hello': 10, 'world': 'value', 'answer': 42.0}
        expected = '{"hello": 10, "world": "value", "answer": 42.0}'
        self.assertEqual(dumps(test_dict), expected)

    def test_dumps_input_not_dict(self):
        with self.assertRaises(TypeError):
            dumps(["not", "a", "dict"])
        with self.assertRaises(TypeError):
            dumps("not a dict")

    def test_dumps_invalid_key(self):
        with self.assertRaises(TypeError) as e:
            dumps({216: "value1"})
        with self.assertRaises(TypeError):
            dumps({42.0: "value1"})

    def test_dumps_unsupported_value(self):
        with self.assertRaises(TypeError):
            dumps({"key1": [1, 2, 3]})

    def test_loads_dumps(self):
        original = {"key1": "value1", "key2": 123, "key3": 45.67}
        json_string = dumps(original)
        self.assertEqual(loads(json_string), original)


if __name__ == "__main__":
    unittest.main()
