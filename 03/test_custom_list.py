import unittest

from custom_list import CustomList


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
        self.assertEqual(custom_ls1 + custom_ls2, CustomList([6, 3, 10, 15]))
        self.assertEqual(empty_cst_ls + empty_cst_ls, CustomList([]))

        # Сложение двух CustomList разной длины
        self.assertEqual(custom_ls1 + custom_ls3, CustomList([22, 1, 3, 7]))
        self.assertEqual(custom_ls3 + custom_ls4, CustomList([19, 5]))
        self.assertEqual(empty_cst_ls + custom_ls4, CustomList([2, 5]))

        # Сложение CustomList и list разной длины
        self.assertEqual(custom_ls1 + ls1, CustomList([9, 8, 3, 7]))
        self.assertEqual(ls1 + custom_ls1, CustomList([9, 8, 3, 7]))

        self.assertEqual(empty_cst_ls + ls1, CustomList([4, 7]))
        self.assertEqual(ls1 + empty_cst_ls, CustomList([4, 7]))

        self.assertEqual(custom_ls1 + ls3, CustomList([12, -4, 16, 7, 8]))
        self.assertEqual(ls3 + custom_ls1, CustomList([12, -4, 16, 7, 8]))

        # Сложение CustomList и list одинаковой длины
        self.assertEqual(custom_ls1 + ls2, CustomList([13, 10, 18, 19]))
        self.assertEqual(ls2 + custom_ls1, CustomList([13, 10, 18, 19]))

        self.assertEqual(empty_cst_ls + empty_ls, CustomList([]))
        self.assertEqual(empty_ls + empty_cst_ls, CustomList([]))

        # Сложение CustomList и int
        self.assertEqual(custom_ls1 + number, CustomList([15, 11, 13, 17]))
        self.assertEqual(number + custom_ls1, CustomList([15, 11, 13, 17]))

        self.assertEqual(custom_ls3 + number, CustomList([27]))
        self.assertEqual(number + custom_ls3, CustomList([27]))

        self.assertEqual(empty_cst_ls + number, CustomList([]))
        self.assertEqual(number + empty_cst_ls, CustomList([]))

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
        self.assertEqual(custom_ls1 - custom_ls2, CustomList([4, -1, -4, -1]))
        self.assertEqual(empty_cst_ls - empty_cst_ls, CustomList([]))

        # Разность двух CustomList разной длины
        self.assertEqual(custom_ls1 - custom_ls3, CustomList([-12, 1, 3, 7]))
        self.assertEqual(custom_ls3 - custom_ls4, CustomList([15, -5]))
        self.assertEqual(empty_cst_ls - custom_ls4, CustomList([-2, -5]))
        self.assertEqual(custom_ls4 - empty_cst_ls, CustomList([2, 5]))

        # Разность CustomList и list разной длины
        self.assertEqual(custom_ls1 - ls1, CustomList([1, -6, 3, 7]))
        self.assertEqual(ls1 - custom_ls1, CustomList([-1, 6, -3, -7]))

        self.assertEqual(empty_cst_ls - ls1, CustomList([-4, -7]))
        self.assertEqual(ls1 - empty_cst_ls, CustomList([4, 7]))

        self.assertEqual(custom_ls1 - ls3, CustomList([-2, 6, -10, 7, -8]))
        self.assertEqual(ls3 - custom_ls1, CustomList([2, -6, 10, -7, 8]))

        # Разность CustomList и list одинаковой длины
        self.assertEqual(custom_ls1 - ls2, CustomList([-3, -8, -12, -5]))
        self.assertEqual(ls2 - custom_ls1, CustomList([3, 8, 12, 5]))

        self.assertEqual(empty_cst_ls - empty_ls, CustomList([]))
        self.assertEqual(empty_ls - empty_cst_ls, CustomList([]))

        # Разность CustomList и int
        self.assertEqual(custom_ls1 - number, CustomList([-5, -9, -7, -3]))
        self.assertEqual(number - custom_ls1, CustomList([5, 9, 7, 3]))

        self.assertEqual(custom_ls3 - number, CustomList([7]))
        self.assertEqual(number - custom_ls3, CustomList([-7]))


if __name__ == '__main__':
    unittest.main()
