import cProfile
from tqdm import tqdm
from timeit import timeit
from project_euler.p70 import primes

N = 1000000

PRIMES_LIST = []
for _p in primes():
    PRIMES_LIST.append(_p)
    if _p > N:
        break


def prime_factorize(n, primes_list):
    factors = {}
    for p in primes_list:
        if p * p > n:
            break
        if n % p == 0:
            c = 0
            while n % p == 0:
                n = n // p
                c += 1
            factors[p] = c

    if n > 1:
        factors[n] = 1

    return factors


def s(factors):
    ss = 1
    for k, v in factors.items():
        kk = 1
        sp = 0
        for i in range(v + 1):
            sp += kk
            kk *= k
        ss *= sp
    return ss


def f(n):
    factors = prime_factorize(n, PRIMES_LIST)
    fn = s(factors)
    return fn - n


def main():
    a = {i: f(i) for i in tqdm(range(2, N))}

    visited = set()

    max_amicable_chain = []
    max_length = 0
    for k, v in tqdm(a.items()):
        if k in visited:
            continue

        amicable_chain = [k]
        ok = True
        while v not in amicable_chain:
            amicable_chain.append(v)
            if v in visited or v not in a or v >= N:
                ok = False
                for i in amicable_chain[:-1]:
                    visited.add(i)
                break
            else:
                v = a[v]

        if not ok:
            continue

        idx = amicable_chain.index(v)
        length = len(amicable_chain) - idx
        amicable_chain = amicable_chain[idx:] + [v]
        if length > max_length:
            max_length = length
            max_amicable_chain = amicable_chain

    print(max_length)
    print(max_amicable_chain)
    print(min(max_amicable_chain))


if __name__ == '__main__':
    with cProfile.Profile(builtins=False) as pr:
        t1 = timeit(main, number=1)
        print(t1)
