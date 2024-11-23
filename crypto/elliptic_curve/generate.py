from ..Mathematic import is_prime
from ..Mathematic.random_prime import random_prime
from ..Mathematic.modpower import modpower
from .EllipticCurve import EllipticCurve

from random import randrange

def generate_secp256k1(a :int ,b:int) -> EllipticCurve:
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    return EllipticCurve(p, a, b, (x, y))


def generate_elliptic_curve_with_number_of_points_being_prime(p: int , a:int ,b :int) -> EllipticCurve:
    assert p >= 8

    if p in [2*255, 2*256]:
        return generate_secp256k1(0,7)

    while True:

        for _ in range(100):
            x = randrange(1, p - 1)
            y = x
            while y == x or (y - x) % p == 0:
                y = randrange(1, p - 1)

            try:
                ec = EllipticCurve(p, a, b, (x, y))
            except AssertionError:
                continue
            if is_prime(ec.num_points_on_curve):
                return ec
