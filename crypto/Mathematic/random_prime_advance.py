from . import random_prime
from ..Mathematic.basic_primes import basic_primes
from ..Mathematic.is_prime_trivial import is_prime_trivial
from ..Mathematic.modpower import modpower
from ..Mathematic.extended_euclidean import gcd
import sys
import random
from typing import Literal

def _select_r(k: int, M: int) -> float:
    if k > 2*M:
        while True:
            s = random.random()
            r = 2 ** (s - 1)
            if (1 - r) * k > M:
                return r
    else:
        return 0.5

def _select_prime_candidate(R: int, q: int, B: int) -> tuple[Literal[True]|Literal["unknown"], int] | tuple[Literal[False], None]:
    n = 2 * R * q + 1
    certainty = is_prime_trivial(n, threshold=B)
    if certainty is not False:
        return certainty, n
    return certainty, None

def random_prime_maurer(k: int) -> int:
    """k: bit length of the prime number to be generated."""
    M = 20

    if k < M:
        return random_prime(lbound=f"{k}b", ubound=f"{k+1}b")
    
    C = 0.2
    B = round(C * k ** 2)
    r = _select_r(k, M)
    q = random_prime_maurer(int(r * k))
    I = int( (2 ** (k-1)) / (2*q) )

    while True:
        while True:
            R = random.randrange(I + 1, 2*I + 1)
            certainty, n = _select_prime_candidate(R, q, B)
            if certainty is False or n is None:
                continue
            break

        if certainty is True:
            return n
        
        for a in basic_primes[:4]:
            R2 = 2 * R
            b = modpower(a, R2, n)
            c = b * modpower(a, R2 * (q-1), n) % n

            if (
                c == 1
                and gcd(b - 1, n) == 1
            ):
                return n

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        k = int(sys.argv[1])
        print(random_prime_maurer(k))
