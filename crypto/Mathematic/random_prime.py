import sys
sys.set_int_max_str_digits(2147483647) # 2^31 - 1

from ..Mathematic.is_prime import is_prime
from ..Mathematic.fact import fact
from ..Mathematic.basic_primes import basic_primes
from ..Mathematic.boundaries import compute_lbound_ubound
from random import randrange
import random
def random_prime(lbound: int|str, ubound: int|str) -> int:
    lbound, ubound = compute_lbound_ubound(lbound, ubound)

    n = randrange(lbound, ubound)
    while not is_prime(n):
        n = randrange(lbound, ubound)
    return n
    # N = n if n % 2 != 0 else n + 1

    # while n < ubound:
    #     if is_prime(n):
    #         return n
    #     n += 2
    # n = N - 2
    # while n > lbound:
    #     if is_prime(n):
    #         return n
    #     n -= 2
    # raise ValueError(f"Could not find a prime between {lbound} and {ubound}")

def random_prime_with_max_num_iters(lbound: int|str, ubound: int|str, max_iters: int) -> int:
    lbound, ubound = compute_lbound_ubound(lbound, ubound, lbound_min=2)

    if ubound <= 2:
        return 2
    
    while True:
        n = randrange(lbound, ubound)
        if is_prime(n):
            return n
        max_iters -= 1
        if max_iters == 0:
            raise StopIteration
def random_prime_with_fact_of_p_minus_1(lbound: int|str, ubound: int|str, max_iters: int|None = None, want_p_congruent_to_3_mod_4: bool = False) -> tuple[int, dict[int, int]]:
    lbound, ubound = compute_lbound_ubound(lbound, ubound, lbound_min=3)

    if ubound <= 15199:
        if ubound <= 3:
            # 3 is itself congruent to 3 mod 4
            return 3, { 2: 1 }

        while True:
            p = random.randrange(lbound, ubound)
            if want_p_congruent_to_3_mod_4 and p % 4 != 3:
                p = max(3, (p + 1) // 4 * 4 + 3)
            if not is_prime(p):
                continue
            return p, fact(p - 1)
    
    threshold = (ubound + lbound) // 2

    iters = max_iters
    while True:
        if iters is not None:
            iters -= 1
            if iters < 0:
                raise StopIteration
        
        fact_of_p_minus_1 = { 2: 1 }
        p_minus_1 = 2

        while p_minus_1 < threshold:
            pk = random.choice(basic_primes)
            if want_p_congruent_to_3_mod_4 and pk == 2:
                continue
            p_minus_1 *= pk
            fact_of_p_minus_1[pk] = fact_of_p_minus_1.get(pk, 0) + 1

        p = p_minus_1 + 1
        if is_prime(p):
            return p, fact_of_p_minus_1
if __name__ == "__main__":

    lbound = 100
    if len(sys.argv) == 2:
        ubound = sys.argv[1]
    elif len(sys.argv) >= 3:
        lbound = sys.argv[1]
        ubound = sys.argv[2]
        if len(sys.argv) == 4:
            max_iters = int( sys.argv[3] )
            print(f"Random prime between {lbound} and {ubound} with max_iters = {max_iters}:")
            print()
            print(random_prime_with_max_num_iters(lbound=lbound, ubound=ubound, max_iters=max_iters))
            sys.exit()
    else:
        ubound = 1000
    
    print(f"Random prime between {lbound} and {ubound}:")
    print()
    print(random_prime(lbound=lbound, ubound=ubound))
