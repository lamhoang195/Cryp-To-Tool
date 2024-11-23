CRYPTO_BITS = 256

RIGHT_PADDING_SIZE = 2
LEFT_PADDING_SIZE = 5

import sys
sys.set_int_max_str_digits(2147483647)
from random import randrange
from copy import deepcopy
from ..template import CryptoCommunicationDriver, CryptoSystem, CryptoSystemTest, Plaintext
from ..elliptic_curve import EllipticCurve, generate_elliptic_curve_with_number_of_points_being_prime
from ..Mathematic.bit_padding import BitPaddingConfig
from ..elliptic_curve import convert_plain_number_to_point_on_curve, convert_point_on_curve_to_plain_number

BIT_PADDING_CONFIG = BitPaddingConfig(LEFT_PADDING_SIZE, RIGHT_PADDING_SIZE)
from ..Mathematic.is_prime import is_prime

def ask_elliptic_curve_interactively() -> EllipticCurve:
    print("Enter parameters of the elliptic curve y^2 = x^3 + ax + b mod p")
    p = int(input("    Enter p: "))
    p_is_prime = is_prime(p) is not False
    a = int(input("    Enter a: "))
    b = int(input("    Enter b: "))
    print("    Enter P (starting point): ")
    P = (
        int(input("        x: ")),
        int(input("        y: "))
    )
    ec = EllipticCurve(p, p_is_prime, a, b, P)
    return ec
class ECElGamalPublicKey:
    def __init__(self, ec: EllipticCurve, B: tuple[int, int]):
        self.ec = ec
        self.B = B
    
    def __repr__(self) -> str:
        return f"ECElGamalPublicKey(ec = {self.ec}, B = {self.B})"

class ECElGamalPrivateKey:
    def __init__(self, ec: EllipticCurve, s: int):
        self.ec = ec
        self.s = s
    
    def __repr__(self) -> str:
        return f"ECElGamalPrivateKey(ec = {self.ec}, s = {self.s})"

class ECElGamalCiphertextPair:
    def __init__(self, M1: tuple[int, int], M2: tuple[int, int]):
        self.M1 = M1
        self.M2 = M2
    
    def __repr__(self) -> str:
        return f"ECElGamalCiphertextPair( M1 = {self.M1} , M2 = {self.M2} )"

class ECElGamalCiphertext:
    def __init__(self, pairs: list[ECElGamalCiphertextPair]):
        self.pairs = deepcopy(pairs)
    
    def __repr__(self) -> str:
        return f"ECElGamalCiphertext(pairs = {self.pairs})"

class ECElGamalCryptoSystem(CryptoSystem[
    ECElGamalPublicKey,
    ECElGamalPrivateKey,
    ECElGamalCiphertext,
]):
    def generate_keypair(self) -> tuple[ECElGamalPublicKey, ECElGamalPrivateKey]:
        ec = generate_elliptic_curve_with_number_of_points_being_prime(CRYPTO_BITS)
        s = randrange(ec.p // 2, ec.p)
        B = ec.get_point_by_index(s)
        pub = ECElGamalPublicKey(ec, B)
        priv = ECElGamalPrivateKey(ec, s)
        return (pub, priv)
    def ask_public_key_interactively(self, prompt: str|None = None) -> ECElGamalPublicKey:
        if prompt is not None:
            print(prompt)
        ec = ask_elliptic_curve_interactively()
        print("Enter B:")
        B = (
            int(input("    x_B: ")),
            int(input("    y_B: "))
        )
        return ECElGamalPublicKey(ec, B)
    
    def ask_plain_text_interactively(self, public_key: ECElGamalPublicKey, prompt: str|None = None) -> Plaintext:
        text_string = input(prompt or "Enter the plaintext message" + " (as text): ")
        return Plaintext.from_string(text_string)
    
    def ask_cipher_text_interactively(self, private_key: ECElGamalPrivateKey, prompt: str|None = None) -> ECElGamalCiphertext:
        print(prompt or "Enter the ciphertext:")
        N = int(input("    Enter the number of pairs: "))
        pairs: list[ECElGamalCiphertextPair] = []
        for i in range(N):
            print(f"Pair {i + 1}:")
            x1 = int(input("    x_M1: "))
            y1 = int(input("    y_M1: "))
            x2 = int(input("    x_M2: "))
            y2 = int(input("    y_M2: "))

            pairs.append(ECElGamalCiphertextPair((x1, y1), (x2, y2)))
        
        return ECElGamalCiphertext(pairs)
    
    def encrypt(self, ec ,B, k :int , M ):
        P = ec.starting_point
        M1 = ec.scale_point(k, P)
        M2 = ec.add_points(M, ec.scale_point(k, B))
        pairs = []
        pairs.append(M1)
        pairs.append(M2)
        return pairs
    
    def decrypt(self,ec,s,M1,M2):
        M = ec.add_points(M2, ec.scale_point(-s, M1))
        return M
    
    def str2plaintext(self, public_key: ECElGamalPublicKey, string: str) -> Plaintext:
        return Plaintext.from_string(string)
    
    def plaintext2str(self, private_key: ECElGamalPrivateKey, plain_text: Plaintext) -> str:
        return plain_text.to_string()

class ECElGamalCryptoSystemTest(CryptoSystemTest[
    ECElGamalPublicKey,
    ECElGamalPrivateKey,
    ECElGamalCiphertext,
]):
    def create_crypto_system(self) -> CryptoSystem[ECElGamalPublicKey, ECElGamalPrivateKey, ECElGamalCiphertext]:
        return ECElGamalCryptoSystem()
def run_CryptoECElGamal():
    driver = CryptoCommunicationDriver.PubkeyCryptoCommunicationDriver(ECElGamalCryptoSystem())
    driver.run()
