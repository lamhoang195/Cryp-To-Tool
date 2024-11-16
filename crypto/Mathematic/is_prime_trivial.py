import sys
sys.set_int_max_str_digits(2147483647) # 2^31 - 1

import typing
import math

def is_prime_trivial(N: int, threshold: int) -> bool|typing.Literal["unknown"]:
    if N <= 1:
        return False
    if N == 2:
        return True

    try:
        SQ = math.sqrt(N)
    except OverflowError:
        real_threshold = threshold
        sure = False
    else:
        if SQ * SQ == N:
            return False

        S = SQ + 1
        threshold += 1

        if N > threshold:
            real_threshold = threshold
            sure = False
        elif S > threshold:
            real_threshold = S
            sure = False
        else:
            real_threshold = S
            sure = True

    for k in range(2, real_threshold):
        if N % k == 0:
            return False

    return True if sure else "unknown"

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        n = int(sys.argv[1])
        print("is prime" if is_prime_trivial(n, 15199) else "is composite")
