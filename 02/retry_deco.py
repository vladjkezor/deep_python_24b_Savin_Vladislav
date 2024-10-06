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
                        f' run "{func.__name__}" with',
                        f'positional args = {args},' if args else "",
                        f'keyword kwargs = {kwargs},' if kwargs else "",
                        f'{attempt=}, {result=}')
                    return result
                except Exception as e:
                    print(
                        f' run "{func.__name__}" with',
                        f'positional args = {args},' if args else "",
                        f'keyword kwargs = {kwargs},' if kwargs else "",
                        f'{attempt=}, exception = {type(e).__name__}')
                    if any(isinstance(e, exc) for exc in exceptions):
                        break
            return None

        return wrapper

    return decorator
