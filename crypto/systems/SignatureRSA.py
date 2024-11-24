SIGNATURE_BITS = (2048, 2048)

import sys
sys.set_int_max_str_digits(2147483647)

from .CryptoRSA import generate_RSA_keypair
from ..Mathematic.modpower import modpower
from ..template import CryptoCommunicationDriver, SignatureSystem, SignatureSystemTest, Plaintext
from ..systems import RSACryptoSystem
def h(x: int) -> int:
    return x

class RSASignatureSignerKey:
    def __init__(self, n: int, d: int) -> None:
        self.n = n
        self.d = d
    
    def __repr__(self) -> str:
        return f"RSASignatureSignerKey(n = {self.n} , a = {self.d})"

class RSASignatureVerifierKey:
    def __init__(self, n: int, e: int) -> None:
        self.n = n
        self.e = e

    def __repr__(self) -> str:
        return f"RSASignatureVerifierKey(n = {self.n} , b = {self.e})"

class RSASignatureSystem(SignatureSystem[RSASignatureSignerKey, RSASignatureVerifierKey]):
    def generate_keypair(self) -> tuple[RSASignatureSignerKey, RSASignatureVerifierKey]:
        (n, e), (n, d) = generate_RSA_keypair(SIGNATURE_BITS[0], SIGNATURE_BITS[1])
        return RSASignatureSignerKey(n, d), RSASignatureVerifierKey(n, e)
    
    def ask_verification_key_interactively(self, prompt: str|None = None) -> RSASignatureVerifierKey:
        print(prompt)
        n, e = int(input("n = ")), int(input("e = "))
        return RSASignatureVerifierKey(n, e)
    
    def sign(self, signer_key: RSASignatureSignerKey, plain_text: Plaintext) -> int:
        n, d = signer_key.n, signer_key.d
        sig = modpower(plain_text, d, n)
        return sig
    
    def verify(self, verifier_key: RSASignatureVerifierKey, plain_text: Plaintext, signature: int) -> bool:
        n, e = verifier_key.n, verifier_key.e
        
        if plain_text % n != modpower(signature, e, n):
            return False
        return True

    def str2plaintext_signer(self, signer_key: RSASignatureSignerKey, string: str) -> Plaintext:
        return Plaintext.from_string(string)

    def str2plaintext_verifier(self, verifier_key: RSASignatureVerifierKey, string: str) -> Plaintext:
        return Plaintext.from_string(string)

class RSASignatureSystemTest(SignatureSystemTest[RSASignatureSignerKey, RSASignatureVerifierKey]):
    def create_signature_system(self) -> RSASignatureSystem:
        return RSASignatureSystem()
def run_CryptoRSA_SignatureRSA():
    driver = CryptoCommunicationDriver.PubkeyCommunicationDriver(RSACryptoSystem(), RSASignatureSystem())
    driver.run()