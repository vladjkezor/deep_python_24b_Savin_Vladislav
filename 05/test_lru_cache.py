import unittest

from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):

    def test_set_and_get(self):
        cache = LRUCache()
        # Проверяем что словарь пуст
        self.assertEqual(cache.cache, {})
        self.assertEqual(cache.get('k1'), None)

        cache.set("k1", "val1")
        self.assertEqual(cache.get('k1'), "val1")

        self.assertEqual(cache.get('k2'), None)

    def test_update_key(self):
        cache = LRUCache()
        cache.set("k1", "val1")
        self.assertEqual(cache.get('k1'), 'val1')
        cache.set("k1", "new_val")
        self.assertEqual(cache.get('k1'), 'new_val')

    def test_ordering(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get('k1'), "val1")
        self.assertEqual(cache.get('k2'), "val2")
        self.assertEqual(cache.get('k3'), None)

        cache.set("k3", "val3")

        self.assertEqual(cache.get('k1'), None)
        self.assertEqual(cache.get('k2'), "val2")
        self.assertEqual(cache.get('k3'), 'val3')

        # Обновляем поряок использования
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get('k2'), "val2")
        self.assertEqual(cache.get('k1'), "val1")
        self.assertEqual(cache.get('k3'), None)

        cache.set("k3", "val3")
        self.assertEqual(len(cache.cache), 2)
        self.assertEqual(cache.get('k1'), 'val1')
        self.assertEqual(cache.get('k2'), None)
        self.assertEqual(cache.get('k3'), 'val3')

    def test_low_limit_cache(self):
        cache = LRUCache(1)
        cache.set("k1", "val1")
        self.assertEqual(cache.get('k1'), 'val1')

        cache.set("k2", "val2")
        self.assertEqual(cache.get('k1'), None)
        self.assertEqual(cache.get('k2'), 'val2')
        self.assertEqual(len(cache.cache), 1)

    def test_bad_limit(self):
        with self.assertRaises(ValueError) as err:
            _ = LRUCache(0)
        self.assertEqual(str(err.exception), 'Limit should be positive')

        with self.assertRaises(ValueError) as err:
            _ = LRUCache(-1)
        self.assertEqual(str(err.exception), 'Limit should be positive')

        with self.assertRaises(TypeError) as err:
            _ = LRUCache(1.5)
        self.assertEqual(str(err.exception), 'Limit should be integer')

        with self.assertRaises(TypeError) as err:
            _ = LRUCache("2")
        self.assertEqual(str(err.exception), 'Limit should be integer')

        with self.assertRaises(TypeError) as err:
            _ = LRUCache([2])
        self.assertEqual(str(err.exception), 'Limit should be integer')


if __name__ == '__main__':
    unittest.main()
