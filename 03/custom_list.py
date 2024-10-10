class CustomList(list):
    def __add__(self, other):
        if isinstance(other, (CustomList, list)):
            result = CustomList()
            for i in range(max(len(other), len(self))):
                result.append((self[i] if i < len(self) else 0) +
                              (other[i] if i < len(other) else 0))
            return result
        if isinstance(other, (int, float)):
            return CustomList([x + other for x in self])
        raise TypeError()

    def __radd__(self, other):
        if isinstance(other, (CustomList, list)):
            return self.__add__(other)
        if isinstance(other, (int, float)):
            return CustomList([x + other for x in self])
        raise TypeError()

    def __sub__(self, other):
        if isinstance(other, (CustomList, list)):
            result = CustomList()
            for i in range(max(len(other), len(self))):
                result.append((self[i] if i < len(self) else 0) -
                              (other[i] if i < len(other) else 0))
            return result
        if isinstance(other, (int, float)):
            return CustomList([x - other for x in self])
        raise TypeError()

    def __rsub__(self, other):
        if isinstance(other, (CustomList, list)):
            result = CustomList()
            for i in range(max(len(other), len(self))):
                result.append((other[i] if i < len(other) else 0) -
                              (self[i] if i < len(self) else 0))
            return result
        if isinstance(other, (int, float)):
            return CustomList([other - x for x in self])
        raise TypeError()

    def __lt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        raise TypeError()

    def __le__(self, other):
        if isinstance(other, CustomList):
            return sum(self) <= sum(other)
        raise TypeError()

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        raise TypeError()

    def __ne__(self, other):
        if isinstance(other, CustomList):
            return sum(self) != sum(other)
        raise TypeError()

    def __gt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) > sum(other)
        raise TypeError()

    def __ge__(self, other):
        if isinstance(other, CustomList):
            return sum(self) >= sum(other)
        raise TypeError()

    def __str__(self):
        return f'{super().__str__()} sum = {str(sum(self))}'
