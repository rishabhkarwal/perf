from functools import lru_cache

@lru_cache(maxsize=None)
def f(n):
    if n < 2: return n

    return f(n - 1) + f(n - 2)
