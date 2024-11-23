import weakref
from time import time


class Book:
    def __init__(self, title, publication_year):
        self.title = title
        self.year = publication_year


class SlotsBook:
    __slots__ = ('title', 'year')

    def __init__(self, title, publication_year):
        self.title = title
        self.year = publication_year


class WeakRefBook:
    def __init__(self, title, publication_year):
        self.title = weakref.ref(title)
        self.year = weakref.ref(publication_year)


class RefClass:
    def __init__(self, value):
        self.value = value


def measure_performance_time(cls, n_instances):
    init_time = 0
    changing_attr_time = 0
    for _ in range(3):
        t_start = time()
        books = [cls(RefClass('title'),
                     RefClass(2010))
                 for _ in range(n_instances)]
        init_time += time() - t_start

        t_start = time()
        for book in books:
            _ = book.title
            _ = book.year
            book.title = RefClass('new_title')
            book.year = RefClass(2024)
        changing_attr_time += time() - t_start

    print(f'{cls.__name__} avg init time = {init_time / 3}')
    print(f'{cls.__name__} avg changing attr time = {changing_attr_time / 3}')


N = 20_000_000
print(f'Number of instances = {N}')
measure_performance_time(Book, N)
measure_performance_time(SlotsBook, N)
measure_performance_time(WeakRefBook, N)
