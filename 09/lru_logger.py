import logging
import logging.config
import json


def create_logger():
    with open('file_logger_config.json', 'r') as file:
        config = json.load(file)
    logging.config.dictConfig(config)
    logger = logging.getLogger('lru_logger')
    return logger


def add_stream(logger):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_form = logging.Formatter('%(asctime)s - %(name)s - '
                                    'line:%(lineno)s - %(levelname)s - '
                                    '%(message)s',
                                    datefmt='%d.%m.%y %H:%M:%S')
    stream_handler.setFormatter(stream_form)
    logger.addHandler(stream_handler)

# lru_logger = create_logger()
# lru_logger.info('twst')
# add_stream(lru_logger)
#
# lru_logger.info('test2')
