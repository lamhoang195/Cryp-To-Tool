
def str2int(m: str) -> int:
    p = 0
    b = 1
    for i in range(len(m) - 1, -1, -1):
        p_i = ((ord(m[i].upper()) - 65) % 26 + 26) % 26
        p += p_i * b
        b *= 26
    return p

def int2str(p: int) -> str:
    m = ""
    while p > 0:
        r = p % 26
        m = chr(r + 65) + m
        p = (p - r) // 26
    return m


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        m = sys.argv[1]
        p = str2int(m)
        print(f"str2int({m}) = {p}")
        m = int2str(p)
        print(f"int2str({p}) = {m}")
    else:
        print("Usage: python strint.py <string>")
        print("Example: python strint.py 'HELLO'")
