SIGNATURE_BITS = 10

import sys
sys.set_int_max_str_digits(2147483647)

from random import randrange
from ..template import CryptoCommunicationDriver, SignatureSystem, SignatureSystemTest, Plaintext
from ..systems import ECElGamalCryptoSystem
from ..elliptic_curve import EllipticCurve, generate_elliptic_curve_with_number_of_points_being_prime
from ..Mathematic import is_prime
from ..Mathematic.extended_euclidean import inverse

from .CryptoECElGamal import ask_elliptic_curve_interactively
def extended_gcd(a, b): 
    if a == 0: 
        return b, 0, 1 
    gcd, x1, y1 = extended_gcd(b % a, a) 
    x = y1 - (b // a) * x1 
    y = x1 
    return gcd, x, y 
def mod_inverse(a, m): 
    gcd, x, y = extended_gcd(a, m) 
    if gcd != 1: 
        raise ValueError("Inverse does not exist") 
    else: 
        return x % m
class ECDSASignatureSignerKey:
    def __init__(self, ec: EllipticCurve, n: int, d: int):
        self.ec = ec
        self.n = n
        self.d = d
    
    def __repr__(self) -> str:
        return f"ECDSASignatureSignerKey(ec = {self.ec}, n = {self.n}, d = {self.d})"

class ECDSASignatureVerifierKey:
    def __init__(self, ec: EllipticCurve, n: int, Q: tuple[int, int]):
        self.ec = ec
        self.n = n
        self.Q = Q
    
    def __repr__(self) -> str:
        return f"ECDSASignatureVerifierKey(ec = {self.ec}, n = {self.n}, Q = {self.Q})"

class ECDSASignatureSystem(SignatureSystem[
    ECDSASignatureSignerKey,
    ECDSASignatureVerifierKey,
]):
    def generate_keypair(self) -> tuple[ECDSASignatureSignerKey, ECDSASignatureVerifierKey]:
        ec = generate_elliptic_curve_with_number_of_points_being_prime(pbits=SIGNATURE_BITS)
        n = ec.num_points_on_curve
        G = ec.starting_point

        nG = ec.scale_point(n, G)
        # print(f"G = {G}, nG = {nG}, n = {n}, p = {ec.p}")
        assert nG == (0, 0)
        d = randrange(1, n)
        Q = ec.scale_point(d, G)

        signer = ECDSASignatureSignerKey(ec, n, d)
        verifier = ECDSASignatureVerifierKey(ec, n, Q)

        return signer, verifier
    def ask_verification_key_interactively(self, prompt: str|None = None) -> ECDSASignatureVerifierKey:
        if prompt is not None:
            print(prompt)
        ec = ask_elliptic_curve_interactively()
        n = ec.num_points_on_curve
        if not is_prime(n):
            n = int(input("Enter the order of starting point G: "))
        print("Enter Q:")
        Q = (
            int(input("    x_Q = ")),
            int(input("    y_Q = ")),
        )
        return ECDSASignatureVerifierKey(ec, n, Q)
    
    def sign(self, ec,n,d, M):
        G = ec.starting_point
        s = 0
        r = 0
        while s == 0:
            r = 0
            k = 0
            while r == 0:
                k = randrange(1, n - 1)
                x1 = ec.scale_point(k, G)[0]
                r = x1 % n
            h = M
            one_per_k_mod_n = mod_inverse(k,n)
            s = (h + d * r) % n * one_per_k_mod_n % n 
        return r, s
    
    def verify(self, verifier_key: ECDSASignatureVerifierKey, plain_text: Plaintext, signature: Plaintext) -> bool:
        ec = verifier_key.ec
        n = verifier_key.n
        Q = verifier_key.Q
        G = ec.starting_point

        def verify_single(r: int, s: int, number: int) -> bool:
            if r <= 0 or r >= n or s <= 0 or s >= n:
                return False
            w = inverse(s, n)
            if w is None:
                return False
            h = number
            u1 = h * w % n
            u2 = r * w % n
            x0 = ec.add_points(ec.scale_point(u1, G), ec.scale_point(u2, Q))[0]
            v = x0 % n

            if v != r:
                print(f"SIGNATURE MISMATCH, v = {v}, r = {r}, s = {s}, number = {number}, n = {n}")
            return v == r
        
        for i in range(len(plain_text.numbers)):
            number = plain_text.numbers[i]
            try:
                r = signature.numbers[2 * i]
                s = signature.numbers[2 * i + 1]
            except IndexError:
                return False
            if not verify_single(r, s, number):
                return False

        return True
    def str2plaintext_signer(self, signer_key: ECDSASignatureSignerKey, string: str) -> Plaintext:
        return Plaintext.from_string(string)
    
    def str2plaintext_verifier(self, verifier_key: ECDSASignatureVerifierKey, string: str) -> Plaintext:
        return Plaintext.from_string(string)

class ECDSASignatureSystemTest(SignatureSystemTest[
    ECDSASignatureSignerKey,
    ECDSASignatureVerifierKey,
]):
    def create_signature_system(self) -> SignatureSystem[ECDSASignatureSignerKey, ECDSASignatureVerifierKey]:
        return ECDSASignatureSystem()

def run_CryptoECElGamal_SignatureECDSA():
    driver = CryptoCommunicationDriver.PubkeyCommunicationDriver(ECElGamalCryptoSystem(), ECDSASignatureSystem())
    driver.run()