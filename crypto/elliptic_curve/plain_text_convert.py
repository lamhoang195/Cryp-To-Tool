from ..Mathematic.bit_padding import BitPaddingConfig, pad, unpad
from . import EllipticCurve
from ..Mathematic.modpower import modpower
from ..Mathematic.legendre import legendre

from random import random

def convert_plain_number_to_point_on_curve(bit_padding_config: BitPaddingConfig, ec: EllipticCurve, number: int) -> tuple[int, int]:
    p, a, b = ec.p, ec.a, ec.b
    f_x = 0
    def check_f_x_being_quadratic_residue_mod_p(x: int) -> bool:
        nonlocal f_x
        f_x = ( modpower(x, 3, p) + a * x + b ) % p
        return legendre(f_x, p) == 1
    
    x = pad(bit_padding_config, number, check_f_x_being_quadratic_residue_mod_p)
    if x is None:
        raise RuntimeError(f"Could not find a suitable x for the number {number}")
    k = (p - 3) // 4
    y = modpower(f_x, k + 1, p)
    if random() < 0.5:
        y = (p - y) % p

    M = (x, y)
    assert ec.is_point_on_curve(M)

    return M

def convert_point_on_curve_to_plain_number(bit_padding_config: BitPaddingConfig, ec: EllipticCurve, M: tuple[int, int]) -> int:
    x = M[0]
    return unpad(bit_padding_config, x)
