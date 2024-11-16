from . import *

import sys
from typing import Callable

CHOICES: dict[str, Callable[[], None]] = {
    "CryptoRSA": run_CryptoRSA,
    "CryptoElGamal": run_CryptoElGamal,
    "CryptoECElGamal": run_CryptoECElGamal,
    "CryptoVigenere": run_CryptoVigenere,
    "CryptoRSA_SignatureRSA": run_CryptoRSA_SignatureRSA,
    "CryptoElGamal_SignatureElGamal": run_CryptoElGamal_SignatureElGamal,
    "CryptoECElGamal_SignatureECDSA": run_CryptoECElGamal_SignatureECDSA,
}
if __name__ == "__main__":


    if len(sys.argv) >= 2:
        choice = sys.argv[1]
        try:
            func = CHOICES[choice]
        except KeyError:
            print(f"Unknown choice: {choice}")
            print(f"Available choices:\n    {"\n    ".join(CHOICES.keys())}")
            sys.exit(1)
        func()
