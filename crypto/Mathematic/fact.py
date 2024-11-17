import sys
from ..Mathematic.is_prime import is_prime
import math
MAX_INT_OF_FLOAT = 2**40 - 1

def find_next_prime_from(x: int) -> int:
    x += 1
    while True:
        if is_prime(x):
            return x
        x += 1

def fact(x: int) -> dict[int, int]:
    if x <= 1:
        raise RuntimeError(f"Invalid op: FACT({x})")
    
    k = 2
    results: dict[int, int] = {}
    x_changed = True
    while x != 1:
        if x_changed:
            sqrt_x = math.sqrt(x)
            if sqrt_x * sqrt_x == x:
                res = fact(sqrt_x)
                for k, v in res.items():
                    results[k] = results.get(k, 0) + v * 2
                break

            if is_prime(x):
                results[x] = 1
                break

        x_changed = False

        if x % k == 0:
            i = 0
            while x % k == 0:
                x = x // k
                i += 1
            results[k] = i
            x_changed = True
        if x == 1: break

        k = find_next_prime_from(k)
    return results
if __name__ == '__main__':

    if len(sys.argv) >= 2:
        n = int(sys.argv[1])
        F = [
            f"({base}^{exponent})"
            for [base, exponent] in fact(n).items()
        ]
        print( 'x'.join(F) )
