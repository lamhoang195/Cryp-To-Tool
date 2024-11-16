import sys

sys.set_int_max_str_digits(2147483647) # 2^31 - 1

def modpower(b: int, n: int, m: int) -> int:
    x = 1
    b %= m
    p = n
    while p != 0:
        r = p % 2
        if r == 1:
            x = (x * b) % m
        b = (b * b) % m
        p = (p // 2)
    return x

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        b = int(sys.argv[1])
        n = int(sys.argv[2])
        m = int(sys.argv[3])
        result = modpower(b, n, m)
        print(f"b ^ n mod m = {result}")
