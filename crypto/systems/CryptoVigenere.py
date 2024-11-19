from ..template.Plaintext import Plaintext
from ..Mathematic.strint import int2str

class VigenereCryptoSystem():
    def __init__(self, key: str = "", ciphertext: str = ""):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.key = key
        self.ciphertext = ciphertext
    def encrypt(self, key: str, plaintext: Plaintext) -> str:
        L = len(key)
        accumulation = ""
        result = ""

        for number in plaintext.numbers:
            string = int2str(number)
            for c in string:
                accumulation += c
                if len(accumulation) == L:
                    for i in range(L):
                        ch = self.alphabet.index(accumulation[i].upper())
                        kh = self.alphabet.index(key[i].upper())
                        new_ch = (ch + kh) % 26
                        result += self.alphabet[new_ch]
                    accumulation = ""

        for i in range(L):
            try:
                ch = self.alphabet.index(accumulation[i].upper())
                kh = self.alphabet.index(key[i].upper())
                new_ch = (ch + kh) % 26
                result += self.alphabet[new_ch]
            except IndexError:
                break

        return result

    def decrypt(self, key: str, ciphertext: str) -> Plaintext:
        L = len(key)
        accumulation = ""
        result = ""

        for c in ciphertext:
            accumulation += c
            if len(accumulation) == L:
                for i in range(L):
                    ch = self.alphabet.index(accumulation[i].upper())
                    kh = self.alphabet.index(key[i].upper())
                    new_ch = (ch - kh) % 26
                    result += self.alphabet[new_ch]
                accumulation = ""

        for i in range(L):
            try:
                ch = self.alphabet.index(accumulation[i].upper())
                kh = self.alphabet.index(key[i].upper())
                new_ch = (ch - kh) % 26
                result += self.alphabet[new_ch]
            except IndexError:
                break

        return Plaintext.from_string(result)
    
    def plaintext2key(self, plaintext: Plaintext) -> str:
        return plaintext.to_string()
    
    def key2plaintext(self, key: str) -> Plaintext:
        return Plaintext.from_string(key)
    
    def str2plaintext(self, key: str, s: str) -> Plaintext:
        return Plaintext.from_string(s)
    
    def plaintext2str(self, key: str, plaintext: Plaintext) -> str:
        return plaintext.to_string()

def run_CryptoVigenere():
    key = input("Please enter a key: ")
    system = VigenereCryptoSystem(key)
    plaintext = Plaintext.from_string(input("Please enter a plaintext: "))
    ciphertext = system.encrypt(key, plaintext)
    print(f"Plaintext: {plaintext.to_string()}")
    print(f"Ciphertext: {ciphertext}")
    decrypted = system.decrypt(key, ciphertext)
    print(f"Decrypted: {decrypted.to_string()}")