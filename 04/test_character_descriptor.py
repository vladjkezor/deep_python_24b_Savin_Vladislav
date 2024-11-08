import unittest

from character_descriptor import Character


class TestCharacter(unittest.TestCase):
    def test_character_creation(self):
        character1 = Character(name="Джон Голт",
                               health=100,
                               mana=50,
                               race="Человек")
        self.assertEqual(character1.name, "Джон Голт")
        self.assertEqual(character1.health, 100)
        self.assertEqual(character1.mana, 50)
        self.assertEqual(character1.race, "Человек")

        character2 = Character("Джон Доу", 40, 60, "Гном")
        self.assertEqual(character2.name, "Джон Доу")
        self.assertEqual(character2.health, 40)
        self.assertEqual(character2.mana, 60)
        self.assertEqual(character2.race, "Гном")

    def test_invalid_name_type(self):
        with self.assertRaises(TypeError) as err:
            _ = Character(name=123, health=100, mana=50, race="Человек")
        self.assertEqual(str(err.exception), 'Name should be string')

    def test_empty_name(self):
        with self.assertRaises(ValueError) as err:
            _ = Character(name="", health=100, mana=50, race="Эльф")
        self.assertEqual(str(err.exception), 'Name should not be empty')

    def test_invalid_health_type(self):
        with self.assertRaises(TypeError) as err:
            _ = Character(name="Джон Голт", health="сто", mana=50, race="Орк")
        self.assertEqual(str(err.exception), 'Health should be integer')

    def test_negative_health(self):
        with self.assertRaises(ValueError) as err:
            _ = Character(name="Славик322", health=-10, mana=50, race="Нежить")
        self.assertEqual(str(err.exception), 'Health should be positive')

        with self.assertRaises(ValueError) as err:
            _ = Character(name="Леголас", health=0, mana=20, race="Эльф")
        self.assertEqual(str(err.exception), 'Health should be positive')

    def test_large_health_value(self):
        character = Character(name="БигБосс",
                              health=10 ** 9,
                              mana=100,
                              race="Гном")
        self.assertEqual(character.health, 10 ** 9)

    def test_invalid_mana_type(self):
        with self.assertRaises(TypeError) as err:
            _ = Character(name="Наруто", health=100, mana="много", race="Гном")
        self.assertEqual(str(err.exception), 'Mana should be integer')

    def test_negative_mana(self):
        with self.assertRaises(ValueError) as err:
            _ = Character(name="Славик322", health=100, mana=-5, race="Нежить")
        self.assertEqual(str(err.exception), 'Mana should be positive')

        with self.assertRaises(ValueError) as err:
            _ = Character(name="Гендальф", health=100, mana=0, race="Человек")
        self.assertEqual(str(err.exception), 'Mana should be positive')

    def test_large_mana_value(self):
        character = Character(name="Дамблдор",
                              health=100,
                              mana=10 ** 9,
                              race="Человек")
        self.assertEqual(character.mana, 10 ** 9)

    def test_invalid_race_type(self):
        with self.assertRaises(TypeError) as err:
            _ = Character(name="Долгопупс", health=30, mana=10, race=['Гном'])

        self.assertEqual(str(err.exception), 'Race name should be string')

    def test_invalid_race_value(self):
        with self.assertRaises(ValueError) as err:
            _ = Character(name="Лонгботтом", health=100, mana=50, race="Маг")

        self.assertEqual(str(err.exception),
                         "Race should be from "
                         "['Человек', 'Эльф', 'Гном', 'Орк', 'Нежить']")

    def test_empty_race(self):
        with self.assertRaises(ValueError) as err:
            _ = Character(name="Unknown", health=100, mana=100, race="")
        self.assertEqual(str(err.exception),
                         'Race should be from '
                         "['Человек', 'Эльф', 'Гном', 'Орк', 'Нежить']")

    def test_str_method(self):
        character = Character(name="Синий трактор",
                              health=10000,
                              mana=5000,
                              race="Нежить")

        expected_str = ("Имя Синий трактор \n"
                        "Раса Нежить \n"
                        "Здоровье 10000 \n"
                        "Мана 5000")
        self.assertEqual(str(character), expected_str)

    def test_changing_value(self):
        test_char = Character(name="Джон Голт",
                               health=100,
                               mana=50,
                               race="Человек")
        self.assertEqual(test_char.name, "Джон Голт")
        self.assertEqual(test_char.health, 100)
        self.assertEqual(test_char.mana, 50)
        self.assertEqual(test_char.race, "Человек")

        # valid value
        test_char.name = 'New_Person4'
        test_char.health = 200
        test_char.mana = 130
        test_char.race = 'Эльф'
        self.assertEqual(test_char.name, "New_Person4")
        self.assertEqual(test_char.health, 200)
        self.assertEqual(test_char.mana, 130)
        self.assertEqual(test_char.race, "Эльф")

if __name__ == '__main__':
    unittest.main()
