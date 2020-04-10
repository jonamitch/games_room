from functools import wraps
import time


def time_func(func):
    @wraps(func)
    def timed_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        string_to_print = "Time to run function '" + func.__name__ + "': " + str(end_time - start_time)
        print(string_to_print)

        return result
    return timed_func
