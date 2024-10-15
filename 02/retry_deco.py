from functools import wraps


def retry_deco(retries=3, exceptions=None):
    if exceptions is None:
        exceptions = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    result = func(*args, **kwargs)
                    print(
                        f'run "{func.__name__}", ',
                        f'positional args = {args}, ' if args else "",
                        f'keyword kwargs = {kwargs}, ' if kwargs else "",
                        f'{attempt=}, {result=}', sep="")
                    return result
                except tuple(exceptions) as e:  # pylint: disable=E0712
                    print(
                        f'run "{func.__name__}", ',
                        f'positional args = {args}, ' if args else "",
                        f'keyword kwargs = {kwargs}, ' if kwargs else "",
                        f'{attempt=}, Normal Exception = {type(e).__name__}',
                        sep="")
                    raise e     # pylint: disable=E0710
                except Exception as e:
                    print(
                        f'run "{func.__name__}", ',
                        f'positional args = {args}, ' if args else "",
                        f'keyword kwargs = {kwargs}, ' if kwargs else "",
                        f'{attempt=}, Exception = {type(e).__name__}', sep="")
                    if attempt == retries:
                        raise e
            return None

        return wrapper

    return decorator
