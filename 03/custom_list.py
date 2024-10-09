class CustomList(list):
    def __add__(self, other):
        if isinstance(other, CustomList):
            result = CustomList()
            for i in range(max(len(other), len(self))):
                result.append((self[i] if i < len(self) else 0) +
                              (other[i] if i < len(other) else 0))
            return result
        if isinstance(other, (int, float)):
            return CustomList([x + other for x in self])
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, CustomList):
            return self.__add__(other)
        if isinstance(other, (int, float)):
            return CustomList([x + other for x in self])
        return NotImplemented
