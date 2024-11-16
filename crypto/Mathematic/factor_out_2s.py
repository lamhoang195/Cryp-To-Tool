import sys
sys.set_int_max_str_digits(2147483647) # 2^31 - 1


def factor_out_2s(N: int) -> tuple[int, int]:
    """Finds d and s such that N = d * 2^s where d is odd."""
    s = 0
    d = N
    while d % 2 == 0:
        d = d // 2
        s += 1
    
    assert 2**s * d == N
    return (d, s)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        n = int(sys.argv[1])
        d, s = factor_out_2s(n)
        print(f"{n} = {d} * 2^{s}")