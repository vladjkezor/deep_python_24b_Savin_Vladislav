import unittest

from filter_reading import reader_with_filter


class TestReaderWithFilter(unittest.TestCase):
    def test_file_not_found(self):
        wrong_filename = 'no_file.txt'
        key_words = ['word']
        stop_words = ['stop']

        with self.assertRaises(FileNotFoundError):
            list(reader_with_filter(wrong_filename, key_words, stop_words))

    def test_case_insensitive(self):
        file_name = 'test_file.txt'
        key_words = ['apple', 'banana']
        stop_words = ['STOP', 'end']

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('APPLE is a fruit\n')
            f.write('BAnaNA is yellow\n')
            f.write('stop\n')
            f.write('here we have End\n')
            f.write('banana End\n')

        expected = ['APPLE is a fruit',
                    'BAnaNA is yellow']

        result = list(reader_with_filter(file_name, key_words, stop_words))
        self.assertEqual(expected, result)

    def test_with_multiple_key_words_in_line(self):
        file_name = 'test_file.txt'
        key_words = ['apple', 'banana']
        stop_words = ['STOP', 'end']

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('apple and banana are sweet')

        expected = ['apple and banana are sweet']

        result = list(reader_with_filter(file_name, key_words, stop_words))
        self.assertEqual(expected, result)

    def test_with_empty_file(self):
        file_name = 'test_file.txt'
        key_words = ['apple', 'banana']
        stop_words = ['STOP', 'end']

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('')

        expected = []

        result = list(reader_with_filter(file_name, key_words, stop_words))
        self.assertEqual(expected, result)

    def test_with_empty_keywords(self):
        file_name = 'test_file.txt'
        key_words = []
        stop_words = ['STOP', 'end']

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('APPLE is a fruit\n')
            f.write('BAnaNA is yellow\n')
            f.write('stop\n')

        expected = []

        result = list(reader_with_filter(file_name, key_words, stop_words))
        self.assertEqual(expected, result)

    def test_equal_key_and_stop_words(self):
        file_name = 'test_file.txt'
        key_words = ['apple', 'banana']
        stop_words = ['apple']

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('APPLE is a fruit\n')
            f.write('BAnaNA is yellow\n')

        expected = ['BAnaNA is yellow']

        result = list(reader_with_filter(file_name, key_words, stop_words))
        self.assertEqual(expected, result)

    def test_partial_word_match(self):
        file_name = 'test_file.txt'
        key_words = ['key']
        stop_words = []

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('keyboard\n')
            f.write('key\n')

        expected = ['key']

        result = list(reader_with_filter(file_name, key_words, stop_words))
        self.assertEqual(expected, result)

    def test_full_line_match(self):
        file_name = 'test_file.txt'
        key_words = ['banana is red']
        stop_words = ['stop key is key']

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('banana is red\n')
            f.write('stop key is key\n')

        expected = []

        result = list(reader_with_filter(file_name, key_words, stop_words))
        self.assertEqual(expected, result)

    def test_file_obj(self):
        file_name = 'test_file.txt'
        key_words = ['is']
        stop_words = ['STOP', 'end']

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('APPLE is a fruit\n')
            f.write('BAnaNA is yellow\n')
            f.write('Is stop\n')

        expected = ['APPLE is a fruit',
                    'BAnaNA is yellow']

        with open(file_name, 'r', encoding='utf-8') as file_obj:
            result = list(reader_with_filter(file_obj, key_words, stop_words))

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
