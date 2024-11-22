
CRYPTO_BITS = 256

RIGHT_PADDING_SIZE = 2
LEFT_PADDING_SIZE = 5

import sys
sys.set_int_max_str_digits(2147483647)

from random import randrange

from ..Mathematic.extended_euclidean import inverse
from ..Mathematic.modpower import modpower
from ..Mathematic.primitive_root import is_primitive_root_fast
from ..Mathematic.random_prime import random_prime_with_fact_of_p_minus_1
from ..template import CryptoCommunicationDriver, CryptoSystem, CryptoSystemTest, Plaintext
from ..Mathematic.bit_padding import pad, unpad, BitPaddingConfig
from ..Mathematic.fact import fact

BIT_PADDING_CONFIG = BitPaddingConfig(LEFT_PADDING_SIZE, RIGHT_PADDING_SIZE)

def convert_plain_number_to_primitive_root(p: int, original_number: int, fact_of_p_minus_1: dict[int, int]) -> int:
    def check_func(candidate: int) -> bool:
        return is_primitive_root_fast(p, candidate, fact_of_p_minus_1)
    padded_number = pad(BIT_PADDING_CONFIG, original_number, check_func)
    if padded_number is None:
        raise RuntimeError(f"Could not find a valid primitive root modulo p = {p} substituting original_number = {original_number}")
    return padded_number

def convert_primitive_root_to_plain_number(primitive_root: int) -> int:
    return unpad(BIT_PADDING_CONFIG, primitive_root)

class ElGamalCiphertextPair:
    def __init__(self, y1: int, y2: int):
        self.y1 = y1
        self.y2 = y2
    
    def __repr__(self) -> str:
        return f"ElGamalCiphertextPair(y1 = {self.y1}, y2 = {self.y2})"

class ElGamalCiphertext:
    def __init__(self, cipher_pairs: list[ElGamalCiphertextPair]):
        self.cipher_pairs = list(cipher_pairs)
    
    def __repr__(self) -> str:
        return f"ElGamalCiphertext({[str(x) for x in self.cipher_pairs]})"

def ElGamal_generate_keypair(pbits: int) -> tuple[tuple[int, int, int], tuple[int, int], dict[int, int]]:
    p, fact_of_p_minus_1 = random_prime_with_fact_of_p_minus_1(lbound=f"{pbits}b", ubound=f"{pbits + 1}b")
    # alpha = p // 2
    alpha = 2
    while not is_primitive_root_fast(alpha, p, fact_of_p_minus_1):
        alpha += 1
    a = random_prime_with_fact_of_p_minus_1(lbound=p // 3, ubound=p - 1)[0]
    beta = modpower(alpha, a, p)

    return (p, alpha, beta), (p, a), fact_of_p_minus_1

class ElGamalCryptoPublicKey:
    def __init__(self, p: int, alpha: int, beta: int):
        self.p = p
        self.alpha = alpha
        self.beta = beta
    
    def __repr__(self) -> str:
        return f"ElGamalCryptoPublicKey(p = {self.p}, alpha = {self.alpha}, beta = {self.beta})"

class ElGamalCryptoPrivateKey:
    def __init__(self, p: int, a: int):
        self.p = p
        self.a = a
    
    def __repr__(self) -> str:
        return f"ElGamalCryptoPrivateKey(p = {self.p}, a = {self.a})"

class ElGamalCryptoSystem(CryptoSystem[
    ElGamalCryptoPublicKey,
    ElGamalCryptoPrivateKey,
    ElGamalCiphertext,
]):
    def generate_keypair(self) -> tuple[ElGamalCryptoPublicKey, ElGamalCryptoPrivateKey]:
        (p, alpha, beta), (p, a), fact_of_p_minus_1 = ElGamal_generate_keypair(CRYPTO_BITS)
        return ElGamalCryptoPublicKey(p, alpha, beta, fact_of_p_minus_1), ElGamalCryptoPrivateKey(p, a)
    
    def ask_public_key_interactively(self, prompt: str|None = None) -> ElGamalCryptoPublicKey:
        print(prompt)
        p = int(input("Enter p: "))
        alpha = int(input("Enter alpha: "))
        beta = int(input("Enter beta: "))
        return ElGamalCryptoPublicKey(p, alpha, beta, fact(p - 1)) # TODO: do partner need to share fact_of_p_minus_1?
    
    def ask_plain_text_interactively(self, public_key: ElGamalCryptoPublicKey, prompt: str|None = None) -> Plaintext:
        s = input((prompt or "Enter plaintext") + " (as string): ")
        return Plaintext.from_string(s)

    def ask_cipher_text_interactively(self, private_key: ElGamalCryptoPrivateKey, prompt: str|None = None) -> ElGamalCiphertext:
        print(prompt)
        N = int(input("Enter number of pairs: "))
        cipher_pairs: list[ElGamalCiphertextPair] = []
        for i in range(0, N):
            print(f"Enter pair {i + 1}: ")
            y1 = int(input("Enter y1: "))
            y2 = int(input("Enter y2: "))
            cipher_pairs.append(ElGamalCiphertextPair(y1, y2))
        return ElGamalCiphertext(cipher_pairs)
    
    def encrypt(self, public_key: ElGamalCryptoPublicKey,k :int  ,plain_text: Plaintext) ->  tuple[int, int]:
        p, alpha, beta = public_key.p, public_key.alpha, public_key.beta
        
        y1 = modpower(alpha, k, p)
        y2 = plain_text * modpower(beta, k, p) % p

        return y1,y2
    
    def decrypt(self, private_key: ElGamalCryptoPrivateKey, cipher_text: ElGamalCiphertext) -> int:
        p, a = private_key.p, private_key.a
        c1 = cipher_text[0]
        c2 = cipher_text[1]
        s = modpower(c1, a, p)
        s = inverse(s, p)
        if s is None:
            raise RuntimeError(f"Could not find s such that y1^a * s = 1 mod p. c1 = {c1}, a = {a}, p = {p}")
        m = c2 * s % p
        return m
    def str2plaintext(self, public_key: ElGamalCryptoPublicKey, string: str) -> Plaintext:
        return Plaintext.from_string(string)
    
    def plaintext2str(self, private_key: ElGamalCryptoPrivateKey, plain_text: Plaintext) -> str:
        return plain_text.to_string()

class ElGamalCryptoSystemTest(CryptoSystemTest[ElGamalCryptoPublicKey, ElGamalCryptoPrivateKey, ElGamalCiphertext]):
    def create_crypto_system(self) -> ElGamalCryptoSystem:
        return ElGamalCryptoSystem()
def run_CryptoElGamal():
    driver = CryptoCommunicationDriver.PubkeyCryptoCommunicationDriver(ElGamalCryptoSystem())
    driver.run()
