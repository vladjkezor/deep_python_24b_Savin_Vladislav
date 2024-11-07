import unittest

from metaclass import CustomMeta


# pylint: disable=W0201
# pylint: disable=E1101

class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


class TestMetaclass(unittest.TestCase):
    def test_class_attrs(self):
        self.assertEqual(50, CustomClass.custom_x)
        with self.assertRaises(AttributeError):
            _ = CustomClass.x

        CustomClass.x = 30
        self.assertEqual(30, CustomClass.custom_x)
        with self.assertRaises(AttributeError):
            _ = CustomClass.x

        CustomClass.custom_x = 15
        self.assertEqual(15, CustomClass.custom_custom_x)
        self.assertEqual(30, CustomClass.custom_x)

        CustomClass.xx = 30
        self.assertEqual(30, CustomClass.custom_xx)
        with self.assertRaises(AttributeError):
            _ = CustomClass.xx

        with self.assertRaises(AttributeError):
            del CustomClass.x

        del CustomClass.custom_xx
        del CustomClass.custom_x
        del CustomClass.custom_custom_x

        CustomClass.x = 50

    def test_class_methods(self):
        def test_func():
            return 42

        CustomClass.test_func = test_func
        self.assertEqual(42, CustomClass.custom_test_func())
        with self.assertRaises(AttributeError):
            _ = CustomClass.test_func()

        del CustomClass.custom_test_func

    def test_instance_attrs(self):
        test_inst1 = CustomClass()
        test_inst2 = CustomClass(34)

        # class attrs
        self.assertEqual(50, test_inst1.custom_x)
        self.assertEqual(50, test_inst2.custom_x)

        with self.assertRaises(AttributeError):
            _ = test_inst1.x
        with self.assertRaises(AttributeError):
            _ = test_inst2.x

        # init attrs
        self.assertEqual(99, test_inst1.custom_val)
        self.assertEqual(34, test_inst2.custom_val)

        with self.assertRaises(AttributeError):
            _ = test_inst1.val
        with self.assertRaises(AttributeError):
            _ = test_inst2.val

        # dynamic add
        test_inst1.dynamic = 500
        with self.assertRaises(AttributeError):
            _ = test_inst1.dynamic

        self.assertEqual(500, test_inst1.custom_dynamic)

    def test_instance_methods(self):
        test_inst1 = CustomClass()

        self.assertEqual(100, test_inst1.custom_line())

        with self.assertRaises(AttributeError):
            _ = test_inst1.line()

        def dynamic_method():
            return 'dynamic'

        test_inst1.dynamic = dynamic_method

        self.assertEqual('dynamic', test_inst1.custom_dynamic())
        with self.assertRaises(AttributeError):
            _ = test_inst1.dynamic()

        with self.assertRaises(AttributeError):
            del test_inst1.dynamic

        del test_inst1.custom_dynamic

    def test_magic(self):
        test_inst1 = CustomClass()

        with self.assertRaises(AttributeError):
            _ = test_inst1.custom___str__()
        # Проверка метода __str__
        self.assertEqual(str(test_inst1), "Custom_by_metaclass")

    def test_instance_independence(self):
        # Создаем два экземпляра с разными значениями
        test_inst1 = CustomClass(99)
        test_inst2 = CustomClass(34)

        self.assertEqual(test_inst1.custom_val, 99)
        self.assertEqual(test_inst2.custom_val, 34)

        # Проверка, что изменение test_inst1 не повлиет на test_inst2
        test_inst1.val = 100
        self.assertEqual(test_inst1.custom_val, 100)
        self.assertEqual(test_inst2.custom_val, 34)

        # Добавление нового атрибута
        test_inst1.dynamic = "new value"
        self.assertEqual(test_inst1.custom_dynamic, "new value")
        with self.assertRaises(AttributeError):
            _ = test_inst2.custom_dynamic


if __name__ == '__main__':
    unittest.main()
# pylint: enable=W0201
# pylint: enable=E1101
