class CustomMeta(type):
    def __new__(mcs, name, bases, class_dict):
        new_dict = {}

        for attr_name, attr_value in class_dict.items():
            attr_name = mcs.is_magic(attr_name)
            new_dict[attr_name] = attr_value

        def custom_setattr(self, key, value):
            key = mcs.is_magic(key)
            object.__setattr__(self, key, value)

        new_dict['__setattr__'] = custom_setattr

        return super().__new__(mcs, name, bases, new_dict)

    def __setattr__(cls, key, value):
        key = cls.is_magic(key)
        return super().__setattr__(key, value)

    @staticmethod
    def is_magic(key):
        if not (key.startswith('__') and key.endswith('__')):
            return f'custom_{key}'
        return key


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
