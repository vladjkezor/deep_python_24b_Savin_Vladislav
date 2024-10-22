import os


def reader_with_filter(file_or_filename, key_words: list, stop_words: list):
    key_words = {word.lower() for word in key_words}
    stop_words = {word.lower() for word in stop_words}

    def read_lines(data):
        for line in data:
            check_words = set(line.lower().split())
            if key_words & check_words and not stop_words & check_words:
                yield line.strip()

    if isinstance(file_or_filename, str):
        if not os.path.isfile(file_or_filename):
            raise FileNotFoundError(f"The file '{file_or_filename}'"
                                    f" does not exist.")

        # Если передано название файла
        with open(file_or_filename, 'r', encoding='utf-8') as file:
            yield from read_lines(file)
    # Если передан файл
    else:
        yield from read_lines(file_or_filename)
