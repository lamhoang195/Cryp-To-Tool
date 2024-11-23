SIGNATURE_BITS = 128 # Signature bits must be less than CRYPTO_BITS, otherwise the signature may not be able to be verified properly

import sys
sys.set_int_max_str_digits(2147483647)

from random import randrange

from ..Mathematic.extended_euclidean import inverse
from ..Mathematic.modpower import modpower
from ..Mathematic.fact import fact
from ..template import CryptoCommunicationDriver, SignatureSystem, SignatureSystemTest, Plaintext
from ..systems import ElGamalCryptoSystem

from .CryptoElGamal import ElGamal_generate_keypair, convert_plain_number_to_primitive_root

def sig_get_gamma_of_number_by_index(sig: Plaintext, index: int) -> int:
    return sig.numbers[2 * index]
    
def sig_get_delta_of_number_by_index(sig: Plaintext, index: int) -> int:
    return sig.numbers[2 * index + 1]

class ElGamalSignatureSignerKey:
    def __init__(self, p: int, alpha: int, a: int, k: int) -> None:
        self.p = p
        self.alpha = alpha
        self.a = a
        self.k = k
    
    def __repr__(self) -> str:
        return f"ElGamalSignatureSignerKey(p = {self.p}, alpha = {self.alpha}, a = {self.a}, k = {self.k})"

class ElGamalSignatureVerifierKey:
    def __init__(self, p: int, alpha: int, beta: int) -> None:
        self.p = p
        self.alpha = alpha
        self.beta = beta

    def __repr__(self) -> str:
        return f"ElGamalSignatureVerifierKey(p = {self.p}, alpha = {self.alpha}, beta = {self.beta})"

class ElGamalSignatureSystem(SignatureSystem[
    ElGamalSignatureSignerKey,
    ElGamalSignatureVerifierKey,
]):
    def generate_keypair(self) -> tuple[ElGamalSignatureSignerKey, ElGamalSignatureVerifierKey]:
        (p, alpha, beta), (p, a), fact_of_p_minus_1 = ElGamal_generate_keypair(SIGNATURE_BITS)
        return ElGamalSignatureSignerKey(p, alpha, a, fact_of_p_minus_1), ElGamalSignatureVerifierKey(p, alpha, beta, fact_of_p_minus_1)
    def ask_verification_key_interactively(self, prompt: str|None = None) -> ElGamalSignatureVerifierKey:
        print(prompt)
        p = int(input("Enter p: "))
        alpha = int(input("Enter alpha: "))
        beta = int(input("Enter beta: "))
        return ElGamalSignatureVerifierKey(p, alpha, beta, fact(p - 1)) # TODO: do partner need to share fact_of_p_minus_1?
    
    def sign(self, signer_key: ElGamalSignatureSignerKey, plain_text: Plaintext) -> tuple[int, int]:
        p, alpha, a, k = signer_key.p, signer_key.alpha, signer_key.a, signer_key.k
        if None in [p, alpha, a, k]:
            raise ValueError("Các giá trị của signer_key không hợp lệ. Một hoặc nhiều giá trị là None.")
        gamal = modpower(alpha, k, p)
        sigma = (inverse(k, p - 1) * (plain_text - a * gamal)) % (p - 1)
        return gamal, sigma
    
    def verify(self, verifier_key: ElGamalSignatureVerifierKey, plain_text: Plaintext, gamal, sigma) -> bool:
        p, alpha, beta = verifier_key.p, verifier_key.alpha, verifier_key.beta
        left_hand_side = modpower(alpha, plain_text, p)
        right_hand_side = (modpower(beta, gamal, p) * modpower(gamal, sigma, p)) % p
        if left_hand_side != right_hand_side:
            return False
        return True
    
    def str2plaintext_signer(self, signer_key: ElGamalSignatureSignerKey, string: str) -> Plaintext:
        return Plaintext.from_string(string)
    
    def str2plaintext_verifier(self, verifier_key: ElGamalSignatureVerifierKey, string: str) -> Plaintext:
        return Plaintext.from_string(string)

class ElGamalSignatureSystemTest(SignatureSystemTest[ElGamalSignatureSignerKey, ElGamalSignatureVerifierKey]):
    def create_signature_system(self) -> ElGamalSignatureSystem:
        return ElGamalSignatureSystem()

def run_CryptoElGamal_SignatureElGamal():
    driver = CryptoCommunicationDriver.PubkeyCommunicationDriver(ElGamalCryptoSystem(), ElGamalSignatureSystem())
    driver.run()