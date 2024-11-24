import weakref
from time import time
import cProfile
import pstats
import io

from memory_profiler import profile


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


@profile
def measure_performance_time(cls, n_instances, n_retries):
    init_time = 0
    changing_attr_time = 0
    for _ in range(n_retries):
        t_start = time()
        books = [cls(RefClass(f'title_{i}'),
                     RefClass(2010))
                 for i in range(n_instances)]
        init_time += time() - t_start

        t_start = time()
        for book in books:
            _ = book.title() if isinstance(book.title, weakref.ref) \
                else book.title
            _ = book.year() if isinstance(book.year, weakref.ref) \
                else book.year
            book.title = RefClass('new_title')
            book.year = RefClass(2024)
        changing_attr_time += time() - t_start

    print(f'{cls.__name__} avg init time = {init_time / n_retries}')
    print(f'{cls.__name__} '
          f'avg changing attr time = {changing_attr_time / n_retries}')


if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()

    N = 10_000_000
    N_RETRIES = 3
    print(f'Number of instances = {N}, Number of retries = {N_RETRIES}')
    measure_performance_time(Book, N, N_RETRIES)
    measure_performance_time(SlotsBook, N, N_RETRIES)
    measure_performance_time(WeakRefBook, N, N_RETRIES)

    pr.disable()
    s = io.StringIO()
    SORT_BY = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(SORT_BY)
    ps.print_stats()
    print(s.getvalue())
