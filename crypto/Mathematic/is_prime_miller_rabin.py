import sys
sys.set_int_max_str_digits(2147483647) # 2^31 - 1
import typing
from ..Mathematic.modpower import modpower
from ..Mathematic.factor_out_2s import factor_out_2s

def is_prime_miller_rabin(N: int, base: int) -> typing.Literal[False]|typing.Literal["likely"]:
    if N % 2 == 0:
        raise RuntimeError(f"This is too trivial")
    if base == 1 or base == N - 1:
        raise RuntimeError(f"Choose another base please. Reason: n is always a probable prime to base 1 and n - 1.")
    
    d, s = factor_out_2s(N - 1)

    x = modpower(base, d, N)
    if x == 1:
        return "likely"

    for _r in range(s):
        if x == N - 1: # x is congruent to -1 mod N
            return "likely"
        x = (x * x) % N
    
    return False
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        n = int(sys.argv[1])
        base = int(sys.argv[2])
        print("is prime" if is_prime_miller_rabin(n, base) else "is composite")
