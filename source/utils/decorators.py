import time


def add_timer(method, name=None):
    if not name:
        name = method.__name__

    def wrapper(*args, **kw):
        start_time = int(round(time.time() * 1000))
        result = method(*args, **kw)
        end_time = int(round(time.time() * 1000))

        print(f"time of {name}: {end_time - start_time} ms")
        return result

    return wrapper
