from timeit import timeit
import numpy as np
from itertools import count, takewhile, combinations
from math import gcd, sqrt
from collections import deque
from tqdm import tqdm
from project_euler.p70 import primes, phi, get_prime_factors
import cProfile
# numerator = 1: denominator ranges from 2 to x (inclusive)
# numerator = 2: denominator belongs to {all odd numbers between 3 and x inclusive
# more generally numerator = y: denominator not divisible by prime factors of y


def proper_fractions_count_1(x):
    c = 0
    for denominator in range(2, x + 1):
        for numerator in range(1, denominator):
            if gcd(numerator, denominator) == 1:
                c += 1
    return c


def proper_fractions_count_2(x):
    prime_gen = primes()
    next(prime_gen)
    p = next(prime_gen)

    c = x - 1 + x - 2
    for denominator in range(3, x + 1):
        if denominator == p:
            c += p - 3
            p = next(prime_gen)
        elif denominator % 2 == 0:
            temp = denominator // 2
            for numerator in range(3, denominator - 1, 2):
                if gcd(numerator, temp) == 1:
                    c += 1
        else:
            for numerator in range(2, denominator - 1):
                if gcd(numerator, denominator) == 1:
                    c += 1
    return c


def proper_fractions_count_3(x):
    prime_gen = primes()
    p = next(prime_gen)

    c = 0
    for denominator in range(2, x + 1):
        if denominator == p:
            c += p - 1
            p = next(prime_gen)
        elif denominator % 2 == 0:
            c += int((np.gcd(np.arange(1, denominator, 2), denominator // 2) == 1).sum())
        else:
            c += int((np.gcd(np.arange(1, denominator), denominator) == 1).sum())
    return c


def proper_fractions_count_4(denom_max):
    prime_gen = primes()
    next(prime_gen)
    one_prime = next(prime_gen)
    p_queue = deque()
    p_list = []
    p_list2 = []
    total = 1
    for denominator in tqdm(range(3, denom_max + 1)):
        if denominator == one_prime:
            total += one_prime - 1
            if one_prime < 1000:
                p_list.append(one_prime)
            else:
                p_list2.append(one_prime)
            one_prime = next(prime_gen)
            continue

        sqrt_denominator = sqrt(denominator)

        if denominator % 2 == 0:
            temp = remove_prime(denominator, 2)
            if temp in p_list or temp in p_list2:
                factor2 = temp
                total += (factor2 - 1) * denominator // 2 // factor2
                continue

            for factor2 in takewhile(lambda x: x <= temp, p_list):
                if denominator % factor2 == 0:
                    # divisible by both 2 and factor2
                    temp2 = remove_prime(temp, factor2)
                    if temp2 == 1:
                        # divisible only by both 2 and factor2
                        total += (factor2 - 1) * denominator // 2 // factor2
                        break
                    offsets = filter(lambda x: x % factor2 != 0, range(1, 2 * factor2, 2))
                    total += sub_count(denominator, 2 * factor2, offsets)
                    break
            else:
                if temp == 1:
                    # only divisible by 2
                    total += denominator // 2
                else:
                    total += sub_count(denominator, 2, [1])

            continue

        for i, factor in enumerate(takewhile(lambda x: x <= sqrt_denominator, p_list)):
            if denominator % factor == 0:
                temp = remove_prime(denominator, factor)
                if temp in p_list or temp in p_list2:
                    factor2 = temp
                    total += (factor - 1) * (factor2 - 1) * denominator // factor // factor2
                    break
                sqrt_temp = sqrt(temp)
                product = factor

                for j, factor2 in enumerate(takewhile(lambda x: x <= sqrt_temp, p_list[i + 1:])):
                    if temp % factor2 == 0:
                        product *= factor2
                        temp2 = remove_prime(temp, factor2)
                        if temp2 in p_list or temp2 in p_list2:
                            factor3 = temp2
                            total += denominator - denominator // factor - denominator // factor2 - denominator // factor3 \
                                     + denominator // factor // factor2 + denominator // factor // factor3 \
                                     + denominator // factor2 // factor3 - denominator // factor // factor2 // factor3
                            break
                        sqrt_temp2 = sqrt(temp2)

                        # divisible by both factor and factor2
                        for factor3 in takewhile(lambda x: x <= sqrt_temp2, p_list[i + j + 2:]):
                            if temp2 % factor3 == 0:
                                temp3 = remove_prime(temp2, factor3)
                                if temp3 == 1:
                                    total += denominator - denominator // factor - denominator // factor2 - denominator // factor3 \
                                             + denominator // factor // factor2 + denominator // factor // factor3 \
                                             + denominator // factor2 // factor3 - denominator // factor // factor2 // factor3
                                    break
                                product *= factor3
                                offsets = filter(lambda x: all(x % f for f in [factor, factor2, factor3]),
                                                 range(1, product))
                                total += sub_count(denominator, product, offsets)
                                break
                        else:
                            offsets = filter(lambda x: all(x % f for f in [factor, factor2]),
                                             range(1, product))
                            total += sub_count(denominator, product, offsets)
                        break
                else:
                    if temp == 1:
                        # only divisible by factor
                        total += (factor - 1) * (denominator // factor)
                    else:
                        offsets = range(1, factor)
                        total += sub_count(denominator, product, offsets)
                break
        else:
            total += int((np.gcd(np.arange(1, denominator, 2), denominator) == 1).sum())
            total += int((np.gcd(np.arange(2, denominator, 2), denominator) == 1).sum())

    return total


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


def remove_prime(number, prime):
    while number % prime == 0:
        number = number // prime
    return number


def sub_count(denominator, factor, h):
    temp = denominator // factor
    return sum(int((np.gcd(np.arange(g, denominator, factor), temp) == 1).sum()) for g in h)


# 8=21
# 10=31
# 100=3043
# 1000=304191
# 10000=30397485
# 100000=3039650753
# 1000000=? solved 303963552391


def T1():
    print(proper_fractions_count(1000000))


if __name__ == '__main__':
    with cProfile.Profile(builtins=False) as pr:
        t1 = timeit(T1, number=1)
        print(t1)

    pr.print_stats(sort='tottime')


# 1/2
# 1/3  2/3
# 1/4       3/4
# 1/5  2/5  3/5  4/5
# 1/6                 5/6
# 1/7  2/7  3/7  4/7  5/7  6/7
# 1/8       3/8       5/8       7/8
# 1/9  2/9       4/9  5/9       7/9  8/9
# 1/10      3/10                7/10      9/10
# 1/11 2/11 3/11 4/11 5/11 6/11 7/11 8/11 9/11 10/11
# 1/12                5/12      7/12                 11/12
# 1/13 2/13 3/13 4/13 5/13 6/13 7/13 8/13 9/13 10/13 11/13 12/13
# 1/14      3/14      5/14                9/14       11/14       13/14
#
