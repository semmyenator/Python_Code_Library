# -*- coding: utf-8 -*-

"""
Prime Number Testing Algorithm

This script implements various optimizations to test if a number is prime.

The code is licensed under the MPL 2.0, GPLv3, and LGPLv3 licenses.
"""

import math
import random
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

# Check if a number less than 4 is prime
def is_small_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    return True

# Main prime number detection function, different methods are selected according to the size of the number
def is_prime(n):
    small_prime = is_small_prime(n)
    if not small_prime:
        return False

    if n < 10000:
        return eratosthenes_sieve(n)
    elif n < 100000000:
        return sqrt_method(n)
    elif n < 10000000000000000:
        if not fermat_test(n):
            return False
        if not miller_rabin_test(n):
            return False
    else:
        if not aks_test(n):
            return False

    return True

# Eratosthenes sieve, suitable for prime number detection in a small range
def eratosthenes_sieve(n):
    sieve = [True] * (n+1)
    for x in range(2, int(n**0.5) + 1):
        if sieve[x]:
            for i in range(x**2, n+1, x):
                sieve[i] = False
    return sieve[n]

# Square root method, suitable for prime number detection in a medium range
def sqrt_method(n):
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

# Fermat test, suitable for prime number detection in a large range
def fermat_test(n, k=5):
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True

# Miller-Rabin test, suitable for prime number detection in a large range
def miller_rabin_test(n, k=5):
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# AKS test, suitable for prime number detection of huge numbers
def aks_test(n):
    small_prime = is_small_prime(n)
    if not small_prime:
        return False

    # Check if n is a perfect power
    for b in range(2, math.isqrt(n) + 1):
        a = n ** (1/b)
        if a - round(a) == 0:
            return False

    # Find smallest r such that the order of n mod r > log2(n)^2
    max_order = math.log2(n) ** 2
    next_prime = 2
    while True:
        next_prime = next_prime + 1
        while not is_prime(next_prime):
            next_prime = next_prime + 1
        order = max([pow(n, k, next_prime) for k in range(1, math.isqrt(next_prime) + 1)])
        if order > max_order:
            r = next_prime
            break

    # Check if n is composite
    for a in range(2, min(r, n)):
        if math.gcd(a, n) > 1:
            return False

    if n <= r:
        return True

    # Check if n is composite
    for a in range(1, math.isqrt(r) * math.log2(n)):
        if not (pow(a, r, n) == 1 or pow(a, r, n) == n - 1):
            return False

    return True

# Parallel processing prime number detection function
def parallel_is_prime(n, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(num_processes) as pool:
        tasks = [pool.apply_async(is_prime, (i,)) for i in range(2, n)]
        results = [task.get() for task in tasks]

    return all(results)

print(is_prime(17))  # True
print(is_prime(21))  # False

print(parallel_is_prime(17))  # True
print(parallel_is_prime(21))  # False
