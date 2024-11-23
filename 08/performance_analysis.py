# import weakref
from time import time
import random as rand

names = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael",
    "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan",
    "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher",
    "Nancy", "Daniel", "Margaret", "Matthew", "Lisa", "Anthony", "Betty",
    "Donald", "Dorothy", "Mark", "Sandra", "Paul", "Ashley", "Steven",
    "Kimberly", "Andrew", "Donna", "Kenneth", "Emily", "Joshua", "Michelle",
    "George", "Carol", "Kevin", "Amanda", "Brian", "Melissa", "Edward",
    "Deborah"]

surnames = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts"]


class Book:

    def __init__(self, title, author, publication_year):
        self.title = title
        self.author = author
        self.year = publication_year

    def __str__(self):
        return f'{self.title}, {self.author}, {self.year}'


class SlotsBook:
    __slots__ = ('title', 'author', 'year')

    def __init__(self, title, author, publication_year):
        self.title = title
        self.author = author
        self.year = publication_year


def measure_performance_time(cls, n_instances):
    t_start = time()
    books = [cls(f'Book_{i}',
                 i,
                 rand.randint(1800, 2025))
             for i in range(n_instances)]

    for book in books:
        book.title = book.title.split('_')[1] + '_book'
        book.year = rand.randint(1500, 1700)

    t_end = time()

    print(f'{cls.__name__} init time = {t_end - t_start}')


measure_performance_time(Book, 10_000_000)
measure_performance_time(SlotsBook, 10_000_000)
