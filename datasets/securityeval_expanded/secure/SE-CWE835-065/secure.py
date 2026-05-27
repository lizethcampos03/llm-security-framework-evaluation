def getFibonacci(n):
    '''
    Compute the n-th fibonacci number using loops only.
    '''
    if n <= 0:
        return 0
    if n == 1 or n == 2:
        return 1
    
    a, b = 1, 1
    i = 2
    while i < n:
        a, b = b, a + b
        i += 1
    return b