# pylint: disable=R0801
class LRUCache:

    def __init__(self, limit=42):
        if not isinstance(limit, int):
            raise TypeError('Limit should be integer')
        if limit <= 0:
            raise ValueError('Limit should be positive')
        self.limit = limit
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            temp = self.cache[key]
            del self.cache[key]
            self.cache[key] = temp
            return temp

        return None

    def set(self, key, value):
        if key in self.cache:
            del self.cache[key]
        if len(self.cache) >= self.limit:
            old_key = next(iter(self.cache))
            del self.cache[old_key]
        self.cache[key] = value
