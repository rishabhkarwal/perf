F = {0: 0, 1: 1}
def f(n):
    if n in F: return F[n]

    # halving step for both branches
    k = n // 2
    # precomputing as used in both cases
    f_k = f(k)

    # optimised bitwise operation for parity check
    if n & 1: # odd identity: F(2k + 1) = F(k)² + F(k + 1)²
        F[n] = (f_k ** 2) + (f(k + 1) ** 2)
        return F[n]

    else: # even identity: F(2k) = F(k) * [2 * F(k - 1) + F(k)]
        F[n] = f_k * ((f(k - 1) << 1) + f_k) # bitwise left-shift for fast multiplication
        return F[n]
