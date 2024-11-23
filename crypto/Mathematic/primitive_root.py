from ..Mathematic.fact import fact
from ..Mathematic.extended_euclidean import inverse
from ..Mathematic.modpower import modpower
import typing
import sympy
def _is_primitive_root_very_trivial(P: int, A: int) -> bool|typing.Literal["unknown"]:
    if P == 1:
        return A == 0

    a = A % P
    if a == 0:
        return False
    return "unknown"

def is_primitive_root_trivial(P: int, A: int) -> bool:
    if P <= 0:
        return False
    a = A % P

    res = _is_primitive_root_very_trivial(P, A)
    if res != "unknown":
        return res

    order = 1
    while a != 1:
        if order > P - 1:
            return False
        a = (a * A) % P
        order += 1
    
    return order == P - 1
def is_primitive_Root(g, p): 
    if sympy.gcd(g, p) != 1: 
        return False 
    factors = sympy.factorint(p - 1) 
    for q in factors: 
        if pow(g, (p - 1) // q, p) == 1: 
            return False 
    return True
def is_primitive_root_fast(P: int, A: int, fact_of_P_minus_1: dict[int, int]) -> bool:
    if P < 10:
        return is_primitive_root_trivial(P, A)
    a = A % P

    res = _is_primitive_root_very_trivial(P, a)
    if res != "unknown":
        return res
    
    P_1 = P - 1
    for pk in fact_of_P_minus_1.keys():
        one_per_pk = inverse(pk, P)
        if one_per_pk is None:
            return False
        if modpower(a, P_1 * one_per_pk % P, P) % P == 1:
            return False
    return True
def find_primitive_root(p: int) -> int: 
    for g in range(2, p): 
        if is_primitive_Root(g, p): 
            return g 
    return -1
def is_primitive_root(P: int, A: int) -> bool:
    if P < 10:
        return is_primitive_root_trivial(P, A)
    a = A % P

    res = _is_primitive_root_very_trivial(P, a)
    if res != "unknown":
        return res
    
    return is_primitive_root_fast(P, a, fact(P - 1))

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        P = int(sys.argv[1])
        A = int(sys.argv[2])
        print(is_primitive_root(P, A))
    else:
        P = 29
        A = 2
