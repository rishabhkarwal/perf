def f(n):
    if n == 0: return 0
    if n == 1: return 1

    def multiply(A, B):
        # unrolled 2x2 matrix multiplication
        return [
            [
                A[0][0] * B[0][0] + A[0][1] * B[1][0], 
                A[0][0] * B[0][1] + A[0][1] * B[1][1]
            ],
            [
                A[1][0] * B[0][0] + A[1][1] * B[1][0], 
                A[1][0] * B[0][1] + A[1][1] * B[1][1]
            ]
        ]

    def power(A, n):
        # computes Aⁿ using binary exponentiation
        M = [[1, 0], [0, 1]]
        while n > 0:
            if n % 2 == 1: M = multiply(M, A)
            A = multiply(A, A)
            n //= 2
        return M

    # transformation matrix
    T = [[1, 1], [1, 0]]
    T_n = power(T, n - 1)
    
    return T_n[0][0]
