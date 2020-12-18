from timeit import timeit
from tqdm import tqdm
from project_euler.p70 import primes, phi, get_prime_factors
import cProfile


def proper_fractions_count(x):
    prime_gen = primes()
    one_prime = next(prime_gen)
    p_list = []

    total = 0
    for denominator in tqdm(range(2, x + 1)):
        if denominator == one_prime:
            total += one_prime - 1
            p_list.append(one_prime)
            one_prime = next(prime_gen)
            continue

        prime_factors = get_prime_factors(denominator, p_list)
        total += phi(denominator, prime_factors)

    return total


def T1():
    print(proper_fractions_count(1000000))


if __name__ == '__main__':
    with cProfile.Profile(builtins=False) as pr:
        t1 = timeit(T1, number=1)
        print(t1)

    pr.print_stats(sort='tottime')
