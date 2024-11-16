
def jacobi(A: int, B: int) -> int:
    if B == 0:
        raise RuntimeError('invalid')
    if B == 1:
        return 1

    if A < 0:
        K = A % B
        return jacobi(K, B)

    if A % B == 0:
        return 0

    if A == 0:
        return 0
    if A == 1:
        return 1

    if B % 2 == 0:
        raise RuntimeError('invalid')
    if A == 2:
        r = (B + 8) % 8
        if r == 1 or r == 7:
            return 1
        elif r == 3 or r == 5:
            return -1
        else:
            raise RuntimeError('invalid')

    if A % 2 == 0:
        # Factor 2
        a = A
        exponent_of_power2 = 0
        while a % 2 == 0:
            a //= 2
            exponent_of_power2 += 1
        return jacobi(a, B) * ( jacobi(2, B) ** exponent_of_power2 )

    if A > B:
        return jacobi(A % B, B)

    if A < B and A % 2 != 0 and B % 2 != 0:
        m = (A + 4) % 4
        n = (B + 4) % 4
        if m == 3 and n == 3:
            return -jacobi(B, A)
        elif m == 1 or n == 1:
            return jacobi(B, A)

    raise RuntimeError('unknown case')

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        A = int(sys.argv[1])
        B = int(sys.argv[2])
        result = jacobi(A, B)
        print(f"jacobi({A}, {B}) = {result}")
    else:
        print("Usage: python jacobi.py <A> <B>")
        print("Example: python jacobi.py 5 7")
