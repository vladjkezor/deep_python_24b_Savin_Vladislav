import unittest

from filter_reading import reader_with_filter


class TestReaderWithFilter(unittest.TestCase):
    def test_file_not_found(self):
        wrong_filename = 'no_file.txt'
        key_words = ['word']
        stop_words = ['stop']

        with self.assertRaises(FileNotFoundError):
            list(reader_with_filter(wrong_filename, key_words, stop_words))

    def test_file_filter(self):
        file_name = 'test_file.txt'
        key_words = ['key', 'banana']
        stop_words = ['stop']

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write('Line with key word\n')
            file.write('Line with two key key words\n')
            file.write('Line with no search words\n')
            file.write('Line with two different key banana words\n')
            file.write('Line with stop and Key word\n')
            file.write('Line with capitalized KEY word\n')
            file.write('Line with stop word\n')

        expected = [
            'Line with key word',
            'Line with two key key words',
            'Line with two different key banana words',
            'Line with capitalized KEY word'
        ]
        result = list(reader_with_filter(file_name, key_words, stop_words))
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
