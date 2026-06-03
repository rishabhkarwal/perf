def f(n):
    if n == 0: return 0
    if n == 1: return 1

    def multiply(A, B):
        # multiplies two 2x2 matrices
        C = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def power(A, n):
        # identity matrix
        M = [[1, 0], [0, 1]]

        for _ in range(n):
            M = multiply(M, A)
            
        return M

    # transformation matrix
    T = [[1, 1], [1, 0]]
    T_n = power(T, n - 1)
    
    return T_n[0][0]
