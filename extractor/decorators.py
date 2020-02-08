import functools


def log(message):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                print(f'{message}...', end=' ')
                result = function(*args, **kwargs)
                print('OK')
                return result
            except Exception:
                print('FAIL')
                raise
        return wrapper
    return decorator
