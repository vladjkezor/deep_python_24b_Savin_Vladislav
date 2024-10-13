class BaseDescriptor:

    def __set_name__(self, owner, name):
        self._name = f'_{name}' # pylint: disable=W0201
        self.public_name = name.capitalize() # pylint: disable=W0201

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self._name, value)

    def validate(self, _):
        return NotImplemented


class String(BaseDescriptor):

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.public_name} should be string")
        if not value:
            raise ValueError(f"{self.public_name} should not be empty")


class Race(BaseDescriptor):
    valid_races = {'Человек', 'Эльф', 'Гном', 'Орк', 'Нежить'}

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.public_name}  name should be string")
        if value not in self.valid_races:
            raise ValueError(f'{self.public_name} should be'
                             f' from {self.valid_races}')


class PosInteger(BaseDescriptor):

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f'{self.public_name} should be integer')
        if value < 0:
            raise ValueError(f'{self.public_name} should be positive')


class Character:
    name = String()
    health = PosInteger()
    mana = PosInteger()
    race = Race()

    def __init__(self, name, health, mana, race):
        self.name = name
        self.health = health
        self.mana = mana
        self.race = race

    def __str__(self):
        return (f'Имя {self.name} \n'
                f'Раса {self.race} \n'
                f'Здоровье {self.health} \n'
                f'Мана {self.mana}')
