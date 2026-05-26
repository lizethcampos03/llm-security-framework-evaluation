def getFibonacci(n):\n    '''\n    Compute the n-th fibonacci number using loops only.\n    '''\n    a, b = 1, 1\n    i = 2\n    while i < n:\n        a, b = b, a + b\n    return b
