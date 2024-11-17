import sys
sys.set_int_max_str_digits(2147483647) # 2^31 - 1

import typing
from ..Mathematic.is_prime_trivial import is_prime_trivial
from ..Mathematic.is_prime_miller_rabin import is_prime_miller_rabin
from sympy import isprime
def is_prime(n: int) :
    return isprime(n)
if __name__ == '__main__':

    if len(sys.argv) >= 2:
        n = int(sys.argv[1])
        print("is prime" if is_prime(n) else "is composite")
