import numpy as np

def f(n):
    if n == 0: return 0
    T = np.array([[1, 1], [1, 0]], dtype=object) # 'object' for arbitrary precision
    T_n = np.linalg.matrix_power(T, n - 1)
    return T_n[0, 0]
