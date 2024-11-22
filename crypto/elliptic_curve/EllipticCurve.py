from ..Mathematic.modpower import modpower
from ..Mathematic.extended_euclidean import inverse
from ..Mathematic.legendre import legendre

def count_points_on_curve_with_prime_modulo(p: int, a: int, b: int) -> int:
    if (
        p == 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
        and a == 0
        and b == 7
    ):
        return 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

    count = 0
    for x in range(p):
        y2 = (x**3 + a*x + b) % p
        if y2 == 0:
            count += 1
            continue
        j = legendre(y2, p)
        if j == 1:
            count += 2
    count += 1
    return count

def add(p: int, a: int, b: int, P: tuple[int, int], Q: tuple[int, int]) -> tuple[int, int]:
        x1, y1 = P
        x2, y2 = Q
        if x1 % p == 0 and y1 % p == 0:
            return Q
        if x2 % p == 0 and y2 % p == 0:
            return P
        
        if (x1 - x2) % p == 0 and (y1 + y2) % p == 0:
            return (0, 0)
        if (x1 - x2) % p == 0 and (y1 - y2) % p == 0:
            i = inverse(2*y1 % p, p)
            if i is None:
                raise RuntimeError(f"Please review this algorithm. FAIL TEST: 2*y1 must be invertible mod p (2*y1 = {2*y1}, p = {p}, y1 = {y1})")
            lmbda = (3*x1**2 + a) * i % p
        else:
            i = inverse((x2 - x1) % p, p)
            if i is None:
                raise RuntimeError(f"Please review this algorithm. FAIL TEST: (x2 - x1) must be invertible mod p (x2 - x1 = {x2 - x1}, p = {p}, x1 = {x1}, x2 = {x2})")
            lmbda = (y2 - y1) * i % p
        x3 = (lmbda**2 - x1 - x2) % p
        y3 = (lmbda * (x1 - x3) - y1) % p
        return (x3, y3)
def double_and_add(p: int, a: int, b: int, s: int, P: tuple[int, int]):

    x = s
    res = (0, 0)
    temp = P
    while x > 0:
        if x % 2 == 1:
            res = add(p, a, b, res, temp) # point add
        temp = add(p, a, b, temp, temp) # double
        x = x // 2
    return res
class EllipticCurve:
    def __init__(self, p: int, a: int, b: int, starting_point: tuple[int, int]):
        self.p = p
        self.a = a
        self.b = b
        self.starting_point = starting_point

        self.num_points_on_curve = count_points_on_curve_with_prime_modulo(p, a, b)

        x, y = starting_point
        assert (4 * modpower(a, 3, p) + 27 * modpower(b, 2, p)) % p != 0
        assert self.is_point_on_curve((x, y))
    
    def __repr__(self) -> str:
        return f"EllipticCurve(p = {self.p} , a = {self.a} , b = {self.b} , starting point P = {self.starting_point})"
    
    def get_point_by_index(self, s: int) -> tuple[int, int]:
        return self.scale_point(s, self.starting_point)
    
    def add_points(self, A: tuple[int, int], B: tuple[int, int]) -> tuple[int, int]:
        return add(self.p, self.a, self.b, A, B)
    
    def scale_point(self, s: int, B: tuple[int, int]) -> tuple[int, int]:
        p = self.p
        a = self.a
        b = self.b
        if s < 0:
            C = (B[0], (p-B[1]) % p)
            s = -s
            x, y = self.scale_point(s, C)
        elif s == 0:
            x, y = (0, 0)
        else:
            x, y = double_and_add(p, a, b, s, B)
        
        assert self.is_point_on_curve((x, y)), f"Point {x, y} is not on the curve {self}"
        return x, y
    
    def search_point(self, B: tuple[int, int], P: tuple[int, int], ubound: int, lbound: int = 0) -> None | int:
        """Returns s such that sP = B. Only search within bounds."""
        if ubound < lbound:
            return None

        o = self.scale_point(lbound, P)
        for s in range(lbound, ubound + 1):
            if o == B:
                return s
            o = self.add_points(o, P)
        return None
    
    def is_point_on_curve(self, point: tuple[int, int]) -> bool:
        x, y = point
        p = self.p
        a = self.a
        b = self.b

        if x % p == 0 and y % p == 0:
            return True

        return (modpower(y, 2, p) - modpower(x, 3, p) - a*x%p - b) % p == 0
