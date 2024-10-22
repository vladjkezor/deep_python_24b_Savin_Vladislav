import unittest

from custom_list import CustomList


def check_equal(ls1, ls2):
    """ Функция для поэлементного сравнения CustomList"""
    if len(ls1) != len(ls2):
        return False
    for item1, item2 in zip(ls1, ls2):
        if item1 != item2:
            return False
    return True


class TestCustomList(unittest.TestCase):
    def test_add(self):
        custom_ls1 = CustomList([5, 1, 3, 7])
        custom_ls2 = CustomList([1, 2, 7, 8])
        custom_ls3 = CustomList([17])
        custom_ls4 = CustomList([2, 5])
        empty_cst_ls = CustomList([])
        empty_ls = []
        ls1 = [4, 7]
        ls2 = [8, 9, 15, 12]
        ls3 = [7, -5, 13, 0, 8]
        number = 10

        # Сложение двух CustomList одинаковой длины

        self.assertTrue(check_equal(custom_ls1 + custom_ls2,
                                    CustomList([6, 3, 10, 15])))
        self.assertTrue(check_equal(empty_cst_ls + empty_cst_ls,
                                    CustomList([])))

        # Сложение двух CustomList разной длины
        self.assertTrue(check_equal(custom_ls1 + custom_ls3,
                                    CustomList([22, 1, 3, 7])))
        self.assertTrue(check_equal(custom_ls3 + custom_ls4,
                                    CustomList([19, 5])))
        self.assertTrue(check_equal(empty_cst_ls + custom_ls4,
                                    CustomList([2, 5])))

        # Сложение CustomList и list разной длины
        self.assertTrue(check_equal(custom_ls1 + ls1,
                                    CustomList([9, 8, 3, 7])))
        self.assertTrue(check_equal(ls1 + custom_ls1,
                                    CustomList([9, 8, 3, 7])))

        self.assertTrue(check_equal(empty_cst_ls + ls1,
                                    CustomList([4, 7])))
        self.assertTrue(check_equal(ls1 + empty_cst_ls,
                                    CustomList([4, 7])))

        self.assertTrue(check_equal(custom_ls1 + ls3,
                                    CustomList([12, -4, 16, 7, 8])))
        self.assertTrue(check_equal(ls3 + custom_ls1,
                                    CustomList([12, -4, 16, 7, 8])))

        # Сложение CustomList и list одинаковой длины
        self.assertTrue(check_equal(custom_ls1 + ls2,
                                    CustomList([13, 10, 18, 19])))
        self.assertTrue(check_equal(ls2 + custom_ls1,
                                    CustomList([13, 10, 18, 19])))

        self.assertTrue(check_equal(empty_cst_ls + empty_ls, CustomList([])))
        self.assertTrue(check_equal(empty_ls + empty_cst_ls, CustomList([])))

        # Сложение CustomList и int
        self.assertTrue(check_equal(custom_ls1 + number,
                                    CustomList([15, 11, 13, 17])))
        self.assertTrue(check_equal(number + custom_ls1,
                                    CustomList([15, 11, 13, 17])))

        self.assertTrue(check_equal(custom_ls3 + number, CustomList([27])))
        self.assertTrue(check_equal(number + custom_ls3, CustomList([27])))

        self.assertTrue(check_equal(empty_cst_ls + number, CustomList([])))
        self.assertTrue(check_equal(number + empty_cst_ls, CustomList([])))

    def test_sub(self):
        custom_ls1 = CustomList([5, 1, 3, 7])
        custom_ls2 = CustomList([1, 2, 7, 8])
        custom_ls3 = CustomList([17])
        custom_ls4 = CustomList([2, 5])
        empty_cst_ls = CustomList([])
        empty_ls = []
        ls1 = [4, 7]
        ls2 = [8, 9, 15, 12]
        ls3 = [7, -5, 13, 0, 8]
        number = 10

        # Разность двух CustomList одинаковой длины
        self.assertTrue(check_equal(custom_ls1 - custom_ls2,
                                    CustomList([4, -1, -4, -1])))
        self.assertTrue(check_equal(empty_cst_ls - empty_cst_ls,
                                    CustomList([])))

        # Разность двух CustomList разной длины
        self.assertTrue(check_equal(custom_ls1 - custom_ls3,
                                    CustomList([-12, 1, 3, 7])))
        self.assertTrue(check_equal(custom_ls3 - custom_ls4,
                                    CustomList([15, -5])))
        self.assertTrue(check_equal(empty_cst_ls - custom_ls4,
                                    CustomList([-2, -5])))
        self.assertTrue(check_equal(custom_ls4 - empty_cst_ls,
                                    CustomList([2, 5])))

        # Разность CustomList и list разной длины
        self.assertTrue(check_equal(custom_ls1 - ls1,
                                    CustomList([1, -6, 3, 7])))
        self.assertTrue(check_equal(ls1 - custom_ls1,
                                    CustomList([-1, 6, -3, -7])))

        self.assertTrue(check_equal(empty_cst_ls - ls1,
                                    CustomList([-4, -7])))
        self.assertTrue(check_equal(ls1 - empty_cst_ls,
                                    CustomList([4, 7])))

        self.assertTrue(check_equal(custom_ls1 - ls3,
                                    CustomList([-2, 6, -10, 7, -8])))
        self.assertTrue(check_equal(ls3 - custom_ls1,
                                    CustomList([2, -6, 10, -7, 8])))

        # Разность CustomList и list одинаковой длины
        self.assertTrue(check_equal(custom_ls1 - ls2,
                                    CustomList([-3, -8, -12, -5])))
        self.assertTrue(check_equal(ls2 - custom_ls1,
                                    CustomList([3, 8, 12, 5])))

        self.assertTrue(check_equal(empty_cst_ls - empty_ls, CustomList([])))
        self.assertTrue(check_equal(empty_ls - empty_cst_ls, CustomList([])))

        # Разность CustomList и int
        self.assertTrue(check_equal(custom_ls1 - number,
                                    CustomList([-5, -9, -7, -3])))
        self.assertTrue(check_equal(number - custom_ls1,
                                    CustomList([5, 9, 7, 3])))

        self.assertTrue(check_equal(custom_ls3 - number,
                                    CustomList([7])))
        self.assertTrue(check_equal(number - custom_ls3,
                                    CustomList([-7])))

    def test_less_than(self):
        custom_ls1 = CustomList([1, 2, 3])
        custom_ls2 = CustomList([0, 1, 2])
        custom_ls3 = CustomList([5])
        custom_ls4 = CustomList([15])
        custom_ls5 = CustomList([])
        custom_ls6 = CustomList([4, 1, 1])

        self.assertTrue(custom_ls2 < custom_ls1)
        self.assertTrue(custom_ls1 < custom_ls4)
        self.assertTrue(custom_ls3 < custom_ls4)
        self.assertTrue(custom_ls5 < custom_ls2)

        self.assertFalse(custom_ls1 < custom_ls2)
        self.assertFalse(custom_ls4 < custom_ls3)
        self.assertFalse(custom_ls4 < custom_ls2)
        self.assertFalse(custom_ls1 < custom_ls3)
        self.assertFalse(custom_ls1 < custom_ls6)

    def test_greater_than(self):
        custom_ls1 = CustomList([1, 2, 3])
        custom_ls2 = CustomList([0, 1, 2])
        custom_ls3 = CustomList([5])
        custom_ls4 = CustomList([15])
        custom_ls5 = CustomList([])
        custom_ls6 = CustomList([4, 1, 1])

        self.assertTrue(custom_ls1 > custom_ls2)
        self.assertTrue(custom_ls4 > custom_ls1)
        self.assertTrue(custom_ls4 > custom_ls3)
        self.assertTrue(custom_ls2 > custom_ls5)

        self.assertFalse(custom_ls2 > custom_ls1)
        self.assertFalse(custom_ls3 > custom_ls4)
        self.assertFalse(custom_ls2 > custom_ls4)
        self.assertFalse(custom_ls3 > custom_ls1)
        self.assertFalse(custom_ls1 > custom_ls6)

    def test_less_equal(self):
        custom_ls1 = CustomList([1, 2, 2])
        custom_ls2 = CustomList([3, 2, 1])
        custom_ls3 = CustomList([6])
        custom_ls4 = CustomList([5])
        empty_ls = CustomList([])

        self.assertTrue(custom_ls1 <= custom_ls2)
        self.assertTrue(custom_ls1 <= custom_ls3)
        self.assertTrue(custom_ls4 <= custom_ls3)
        self.assertTrue(empty_ls <= custom_ls2)

        self.assertFalse(custom_ls2 <= custom_ls1)
        self.assertFalse(custom_ls3 <= custom_ls1)
        self.assertFalse(custom_ls1 <= empty_ls)

    def test_greater_equal(self):
        custom_ls1 = CustomList([2, 6])
        custom_ls2 = CustomList([3, 2, 1])
        custom_ls3 = CustomList([2, 1, 3])
        custom_ls4 = CustomList([6])
        custom_ls5 = CustomList([5])
        empty_ls = CustomList([])

        self.assertTrue(custom_ls1 >= custom_ls2)
        self.assertTrue(custom_ls1 >= custom_ls4)
        self.assertTrue(custom_ls2 >= custom_ls3)
        self.assertTrue(custom_ls5 >= empty_ls)

        self.assertFalse(custom_ls2 >= custom_ls1)
        self.assertFalse(custom_ls5 >= custom_ls4)
        self.assertFalse(empty_ls >= custom_ls3)

    def test_equal(self):
        custom_ls1 = CustomList([1, 2, 3])
        custom_ls2 = CustomList([3, 2, 1])
        custom_ls3 = CustomList([6])
        custom_ls4 = CustomList([5, 3])
        empty_ls = CustomList([])

        self.assertTrue(custom_ls1 == custom_ls2)
        self.assertTrue(custom_ls1 == custom_ls3)
        self.assertTrue(empty_ls == CustomList([]))

        self.assertFalse(custom_ls4 == custom_ls2)
        self.assertFalse(empty_ls == custom_ls3)

    def test_not_equal(self):
        custom_ls1 = CustomList([1, 2, 3])
        custom_ls2 = CustomList([2, 2, 1])
        custom_ls3 = CustomList([8])
        custom_ls4 = CustomList([5, 3])
        empty_ls = CustomList([])

        self.assertTrue(custom_ls1 != custom_ls2)
        self.assertTrue(custom_ls1 != custom_ls3)
        self.assertTrue(empty_ls != custom_ls2)

        self.assertFalse(custom_ls4 != custom_ls3)
        self.assertFalse(empty_ls != CustomList([]))

    def test_comparison_invalid_type(self):
        custom_ls1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            _ = custom_ls1 < "string"
        with self.assertRaises(TypeError):
            _ = custom_ls1 <= {"a": 1}
        with self.assertRaises(TypeError):
            _ = custom_ls1 == 100
        with self.assertRaises(TypeError):
            _ = custom_ls1 != [1, 2, 3]
        with self.assertRaises(TypeError):
            _ = custom_ls1 > "string"
        with self.assertRaises(TypeError):
            _ = custom_ls1 >= {"a": 1}

    def test_add_invalid_type(self):
        custom_ls1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            _ = custom_ls1 + "string"
        with self.assertRaises(TypeError):
            _ = custom_ls1 + {"a": 1}
        with self.assertRaises(TypeError):
            _ = "string" + custom_ls1

    def test_sub_invalid_type(self):
        custom_ls1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            _ = custom_ls1 - "string"
        with self.assertRaises(TypeError):
            _ = custom_ls1 - {"a": 1}
        with self.assertRaises(TypeError):
            _ = "string" - custom_ls1

    def test_str(self):
        custom_ls1 = CustomList([1, 2, 3])
        custom_ls2 = CustomList([8])
        custom_ls3 = CustomList([-5, -14])
        empty_ls = CustomList([])

        self.assertEqual(str(custom_ls1), '[1, 2, 3] sum = 6')
        self.assertEqual(str(custom_ls2), '[8] sum = 8')
        self.assertEqual(str(custom_ls3), '[-5, -14] sum = -19')
        self.assertEqual(str(empty_ls), '[] sum = 0')

    def test_origin_lists_are_unchanged(self):
        custom_ls1 = CustomList([1, 2, 3])
        custom_ls2 = CustomList([8])
        custom_ls3 = CustomList([-5, -14])
        custom_ls4 = CustomList([6, 8, 10])
        empty_ls = CustomList([])
        ls = [2, 34, 11]
        number = 42

        _ = custom_ls1 + custom_ls2
        self.assertTrue(check_equal(custom_ls1, CustomList([1, 2, 3])))
        self.assertTrue(check_equal(custom_ls2, CustomList([8])))

        _ = custom_ls3 - custom_ls4
        self.assertTrue(check_equal(custom_ls3, CustomList([-5, -14])))
        self.assertTrue(check_equal(custom_ls4, CustomList([6, 8, 10])))

        _ = custom_ls1 + empty_ls
        self.assertTrue(check_equal(empty_ls, CustomList([])))
        self.assertTrue(check_equal(custom_ls1, CustomList([1, 2, 3])))

        _ = ls + empty_ls
        self.assertTrue(check_equal(empty_ls, CustomList([])))
        _ = empty_ls - ls
        self.assertTrue(check_equal(empty_ls, CustomList([])))
        _ = number + empty_ls
        self.assertTrue(check_equal(empty_ls, CustomList([])))
        _ = empty_ls - number
        self.assertTrue(check_equal(empty_ls, CustomList([])))

        _ = custom_ls2 + ls
        self.assertTrue(check_equal(custom_ls2, CustomList([8])))
        _ = custom_ls2 - ls
        self.assertTrue(check_equal(custom_ls2, CustomList([8])))

        _ = number + custom_ls4
        self.assertTrue(check_equal(custom_ls4, CustomList([6, 8, 10])))
        _ = custom_ls4 - number
        self.assertTrue(check_equal(custom_ls4, CustomList([6, 8, 10])))


if __name__ == '__main__':
    unittest.main()
