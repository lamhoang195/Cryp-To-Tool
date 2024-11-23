from flask import Blueprint, render_template,request,flash,jsonify
from flask_login import login_required
from crypto.Mathematic.is_prime import is_prime
import random
from math import gcd
from crypto.systems.CryptoElGamal import generate_ELGAMAL_privatekey, generate_ELGAMAL_publickey, ElGamalCryptoSystem, ElGamalCryptoPublicKey, ElGamalCryptoPrivateKey, ElGamalCiphertextPair
from crypto.Mathematic.random_prime import random_prime
from crypto.systems.SignatureElGamal import SIGNATURE_BITS, ElGamalSignatureVerifierKey, ElGamalSignatureSignerKey, ElGamalSignatureSystem
from crypto.template.Plaintext import Plaintext

elgamal_signature = Blueprint('elgamal_signature', __name__)

ELGAMAL = ElGamalCryptoSystem()
ELGAMAL_SIG = ElGamalSignatureSystem()

@elgamal_signature.route('/genkeya', methods=['POST'])
def elgamal_sig_genkeyA():
    try:
        p_a = int(request.form['p_a'])
        alpha_a = int(request.form['alpha_a'])
        a_a = int(request.form['a_a'])
        if not (is_prime(p_a)):
            return jsonify({'error': 'Both p_a must be prime numbers.'})
        if not (isinstance(p_a, int)):
            return jsonify({'error': 'p_a must be integers.'})
        p_a, alpha_a, beta_a = generate_ELGAMAL_publickey(p_a, alpha_a, a_a)
        print(p_a, alpha_a, a_a, beta_a)
        return jsonify({'p_a': str(p_a) , 'alpha_a': str(alpha_a), 'beta_a': str(beta_a), "a_a": str(a_a)})
    except Exception as e:
        return jsonify({'error': str(e)})

@elgamal_signature.route('/genkeyb', methods=['POST'])
def elgamal_sig_genkeyB():
    try:
        p_b = int(request.form['p_b'])
        alpha_b = int(request.form['alpha_b'])
        a_b = int(request.form['a_b'])
        if not (is_prime(p_b)):
            return jsonify({'error': 'Both p_b must be prime numbers.'})
        if not (isinstance(p_b, int)):
            return jsonify({'error': 'p_b bmust be integers.'})
        p_b, alpha_b, beta_b = generate_ELGAMAL_publickey(p_b, alpha_b, a_b)
        print(p_b, alpha_b, a_b, beta_b)
        return jsonify({'p_b': str(p_b) , 'alpha_b': str(alpha_b), 'beta_b': str(beta_b), "a_b": str(a_b)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@elgamal_signature.route('/genprimea', methods=['POST'])
def genprimeA():
    try:
        if not request.form['bits'].isdigit():
            return jsonify({'error': 'Bits must be a positive integer.'})
        if int(request.form['bits']) < 1:
            return jsonify({'error': 'Bits must be a positive integer.'})
        bits = int(request.form['bits'])
        p_a = str(random_prime(lbound=2**bits, ubound=2 ** (bits + 1)))
        return jsonify({'p_a': p_a})
    except Exception as e:
        return jsonify({'error': str(e)})

@elgamal_signature.route('/genprimeb', methods=['POST'])
def genprimeB():
    try:
        if not request.form['bits'].isdigit():
            return jsonify({'error': 'Bits must be a positive integer.'})
        if int(request.form['bits']) < 1:
            return jsonify({'error': 'Bits must be a positive integer.'})
        bits = int(request.form['bits'])
        p_b = str(random_prime(lbound=2**bits, ubound=2 ** (bits + 1)))
        return jsonify({'p_b': p_b})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@elgamal_signature.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        k = int(request.form['k'])
        m = int(request.form['m'])
        p_b = int(request.form['p_b'])
        alpha_b = int(request.form['alpha_b'])
        beta_b = int(request.form['beta_b'])
        if m < 0 or m >= p_b:
            return jsonify({'error': 'Message m must be between 0 and n-1.'})
        public_key = ElGamalCryptoPublicKey(p_b, alpha_b, beta_b)
        y1, y2 = ELGAMAL.encrypt(public_key, k, m)
        return jsonify({'y1': str(y1), 'y2': str(y2)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@elgamal_signature.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        y1 = int(request.form['y1'])
        y2 = int(request.form['y2'])
        p_b = int(request.form['p_b'])
        a_b = int(request.form['a_b'])
        if not (is_prime(p_b)):
            return jsonify({'error': 'p_b must be a prime number.'})
        if not (isinstance(p_b,int)):
            return jsonify({'error': 'p must be an integer.'})
        private_key = ElGamalCryptoPrivateKey(p_b, a_b)
        m = ELGAMAL.decrypt(private_key, [y1, y2])
        return jsonify({'m': str(m)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@elgamal_signature.route('/signature', methods=['POST'])
def signature():
    try:
        m = int(request.form['m'])
        p_a = int(request.form['p_a'])
        alpha_a = int(request.form['alpha_a'])
        a_a = int(request.form['a_a'])
        k2 = random.randint(1, p_a - 1)
        while gcd(k2, p_a - 1) != 1:
            k2 = random.randint(1, p_a - 1)
        if not all([m, p_a, alpha_a, a_a, k2]):
            raise ValueError("Vui lòng nhập đầy đủ các giá trị m, p_a, alpha_a, a_a, k2.")
        signer_key = ElGamalSignatureSignerKey(p_a, alpha_a, a_a, k2)
        gamal, sigma = ELGAMAL_SIG.sign(signer_key, m)
        return jsonify({'k2': str(k2),'gamal': str(gamal), 'sigma': str(sigma)})
    except Exception as e:
        return jsonify({'error': str(e)})

@elgamal_signature.route('/verify', methods=['POST'])
def verify():
    try:
        m = int(request.form['m'])
        p_a =  int(request.form['p_a'])
        alpha_a = int(request.form['alpha_a'])
        beta_a = int(request.form['beta_a'])
        gamal = int(request.form['gamal'])
        sigma = int(request.form['sigma'])
        verifier_key = ElGamalSignatureVerifierKey(p_a, alpha_a, beta_a)
        veri = ELGAMAL_SIG.verify(verifier_key, m, gamal, sigma)
        return jsonify({'veri': veri})
    except Exception as e:
        return jsonify({'error': str(e)})

@elgamal_signature.route('/', methods=['POST'])
def convert():
    try:
        plain = request.form['plain']
        plain = ELGAMAL.str2plaintext(None, plain)
        plain = str(plain)
        return jsonify({'plain': plain})
    except Exception as e:
        return jsonify({'error': str(e)})

