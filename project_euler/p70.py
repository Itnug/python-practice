# n/φ(n) must produce minimum

# φ(n) < n

# φ(p) = p-1

# φ(2n) < n =>  N/φ(N) > 2

# φ(3n) < 2n =>  N/φ(N) > 3/2 = 1.5 

# φ(5n) < 4n => N/φ(N) > 5/4 = 1.25

# φ(87109)=79180 ~~~~ n/φ(n) = 1.1001389239707

from math import gcd
from timeit import timeit
from itertools import count
import numpy as np
from tqdm import tqdm
import cProfile


def primes():
    yield 2
    mem = {}
    for i in count(3, 2):
        if i in mem:
            for k in mem[i]:
                mem.setdefault(i + k, []).append(k)
            del mem[i]
        else:
            yield i
            mem[i + i + i] = [i + i]


def phi_1(n):
    if n == 1:
        return 1
    c = 1
    for i in range(2, n):
        if gcd(i, n) == 1:
            c += 1
    return c


def phi_2(n):
    return (np.gcd(np.arange(2, n), n) == 1).sum() + 1


def is_perm(a, b):
    return sorted(str(a)) == sorted(str(b))


def skip(n, p_array):
    return np.any(n % p_array == 0)


def prime_factorize(n, primes_list):
    prime_factors = []
    i = 1
    while n != 1:
        c = 0
        p = primes_list[i]
        i += 1
        while n % p == 0:
            c += 1
            n //= p

        if c > 0:
            prime_factors.append((p,c))

    return prime_factors


def phi(n, primes_list):
    prime_factors = prime_factorize(n, primes_list)
    product = 1
    for p, k in prime_factors:
        product *= (p**(k-1)) * (p - 1)
    return product


def main():
    start = timeit.default_timer()

    p_list = []
    for i in primes():
        if i / (i-1) < 1.0012471656911804:
            break
        p_list.append(i)
    p_array = np.array(p_list)
    min_m = 9999
    min_n = 1
    for n in tqdm(range(3298093, 10000000, 2)):
        # 2868469
        if skip(n, p_array):
            continue
        phi_n = phi_2(n)
        if is_perm(n, phi_n):
            m = n/phi_n
            split = timeit.default_timer()
            if m < min_m:
                min_n = n
                min_m = m
                print(n, phi_n, m, split-start, '\t!')
            else:
                print(n, phi_n, m, split-start)

    print(min_n)

def main2(max_n):
    primes_gen = primes()
    p = next(primes_gen)
    primes_list = [p]
    p = next(primes_gen)

    min_n = 3
    min_m = 2
    for n in tqdm(range(3, max_n, 2)):
        if n == p:
            primes_list.append(p)
            p = next(primes_gen)
            continue
        if any(n % x == 0 for x in [3, 5, 7, 11]):
            continue
        phi_n = phi(n, primes_list)
        if is_perm(n, phi_n):
            m = n / phi_n
            if m < min_m:
                min_m = m
                min_n = n
                print(n, phi_n, m)
    return min_n

def T1():
    print("answer =", main2(10000000))


with cProfile.Profile() as pr:
    t1 = timeit(T1, number=1)
    print(t1)

pr.print_stats(sort='cumtime')
# print(phi(87109, primes()))