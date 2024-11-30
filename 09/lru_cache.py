# pylint: disable=R0801
import argparse
from lru_logger import create_logger, add_stream

lru_logger = create_logger()


class LRUCache:

    def __init__(self, limit=42):
        if not isinstance(limit, int):
            lru_logger.error('Limit not integer')
            raise TypeError('Limit should be integer')
        if limit <= 0:
            lru_logger.error('Limit not positive')
            raise ValueError('Limit should be positive')
        self.limit = limit
        self.cache = {}
        lru_logger.info('LRUCache initialized with limit %s', self.limit)

    def get(self, key):
        if key in self.cache:
            temp = self.cache[key]
            del self.cache[key]
            self.cache[key] = temp
            lru_logger.info('Key %s accessed successfully', key)
            lru_logger.debug('cache = %s', self.cache)
            return temp
        lru_logger.warning('Key %s is not in the cache', key)
        return None

    def set(self, key, value):
        if key in self.cache:
            del self.cache[key]
            self.cache[key] = value
            lru_logger.info('Key %s updated with new value %s', key, value)
        else:
            if len(self.cache) >= self.limit:
                old_key = next(iter(self.cache))
                del self.cache[old_key]
                lru_logger.info('Cache limit reached. '
                                'Oldest key %s removed', old_key)
            self.cache[key] = value
            lru_logger.info('Key %s added to cache with value %s', key, value)

        lru_logger.debug('cache = %s', self.cache)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stdout', action='store_true')
    parser.add_argument('-f', '--filter', action='store_true')
    args = parser.parse_args()

    if args.stdout:
        add_stream(lru_logger)
    if args.filter:
        pass



