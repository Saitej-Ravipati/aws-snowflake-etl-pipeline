import time
from functools import wraps
from src.utils.logging import get_logger

logger = get_logger("timeit")


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} took {elapsed:.2f}s")
        return result

    return wrapper
