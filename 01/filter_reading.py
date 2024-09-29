import os


def reader_with_filter(filename: str, key_words: list, stop_words: list):
    key_words = {word.lower() for word in key_words}
    stop_words = {word.lower() for word in stop_words}
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"The file '{filename}' does not exist.")
    with open(filename, 'r', encoding='utf-8') as text:
        for line in text:
            words_to_check = set(line.lower().split())
            if key_words & words_to_check and not stop_words & words_to_check:
                yield line.strip()
