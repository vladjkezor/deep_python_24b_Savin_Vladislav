import cProfile
import pstats
import io
from functools import wraps


def profile_deco(func):
    pr = cProfile.Profile()

    @wraps(func)
    def wrapper(*args, **kwargs):
        pr.enable()
        try:
            result = func(*args, *kwargs)
            return result
        finally:
            pr.disable()

    def print_stat():
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

    wrapper.print_stat = print_stat

    return wrapper
