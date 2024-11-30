import logging
import logging.config
import json


def create_logger():
    with open('file_logger_config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    logging.config.dictConfig(config)
    logger = logging.getLogger('lru_logger')
    return logger


def add_stream(logger):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_form = logging.Formatter('%(asctime)s - %(name)s - '
                                    'line:%(lineno)s - %(levelname)-8s - '
                                    '%(message)s',
                                    datefmt='%d.%m.%y %H:%M:%S')
    stream_handler.setFormatter(stream_form)
    logger.addHandler(stream_handler)


def add_filter(logger):
    def custom_filter(record):
        """Отбрасывает записи с четным числом слов"""
        return len(record.msg.split()) % 2 != 0

    logger.addFilter(custom_filter)
    return logger
