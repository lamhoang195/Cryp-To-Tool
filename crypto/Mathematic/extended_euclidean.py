import sys
sys.set_int_max_str_digits(2147483647) # 2^31 - 1

def extended_euclidean(a: int, b: int) -> tuple[int, int, int, int]:
    """Returns (gcd, inverse, x, y)"""
    B = b

    if b == 0:
        return (a, -1, 1, 0)

    x1 = 0
    x2 = 1
    y1 = 1
    y2 = 0

    while b > 0:
        q = a // b
        x = x2 - q * x1
        y = y2 - q * y1

        r = a % b
        a = b
        b = r
        
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y

    d = a
    inverse = (x2 + B) % B if d == 1 else 1
    x = x2
    y = y2
    return (d, inverse, x, y)

def gcd(a: int, b: int) -> int:
    while b > 0:
        r = a % b
        a = b
        b = r
    return a

def inverse(a: int, b: int) -> int:
    return extended_euclidean(a, b)[1]

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        a = sys.argv[1]
        b = sys.argv[2]
    else:
        a = input("Enter a = ")
        b = input("Enter b = ")

    a, b = int(a), int(b)

    if a < 0 or b < 0:
        raise RuntimeError("Invalid parameters")

    d, inv, x, y = extended_euclidean(a, b)
    print(f"d = gcd(a, b) = {d}")
    print(f"x = {x}")
    print(f"y = {y}")
    print(f"inverse = {inv if inv is not None else 'N/A'}")
