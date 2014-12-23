def primes(n=10):
    nump = range(2, n+1)
    for i in range(2, int((n**0.5)+1)):
        nump = filter(lambda x: x == i or x % i, nump)
    return nump

print(primes())
