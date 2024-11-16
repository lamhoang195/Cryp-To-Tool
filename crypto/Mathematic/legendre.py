from ..Mathematic.modpower import modpower

def legendre(A: int, B: int) -> int:
    if B % 2 == 0:
        raise RuntimeError(f"invalid B = {B}")
    
    if B == 1:
        return 1
    
    if A % B == 0:
        return 0
    
    if A == 1:
        return 1
    
    r = modpower(A % B, (B - 1) // 2, B)
    if r == 1:
        return 1
    elif r == B - 1:
        return -1
    else:
        return 0

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        A = int(sys.argv[1])
        B = int(sys.argv[2])
        result = legendre(A, B)
        print(f"legendre({A}, {B}) = {result}")
    else:
        print("Usage: python legendre.py <A> <B>")
        print("Example: python legend")
