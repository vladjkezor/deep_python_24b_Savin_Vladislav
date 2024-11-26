import logging
import logging.config

conf = {
    'version': 1,
    'formatters': {
        "file_form": {
            'format': "%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s",
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'file_form',
            'filename': 'cache.log',
            'mode': 'w'
        },
    },
    'loggers': {
        'lru_logger': {
            'level': 'DEBUG',
            'handlers': ['file_handler'],
            'propagate': False
        },
    },
}


def add_stream(logger):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_form = logging.Formatter('%(process)d\t%(asctime)s\t%(levelname)s\t'
                                    '%(name)s\t%(message)s')
    stream_handler.setFormatter(stream_form)
    logger.addHandler(stream_handler)


logging.config.dictConfig(conf)
lru_logger = logging.getLogger('lru_logger')
