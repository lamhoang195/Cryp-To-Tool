from flask import Blueprint, render_template,request,flash,jsonify
from flask_login import login_required
from crypto.Mathematic.is_prime import is_prime
from crypto.systems.CryptoRSA import generate_RSA_privatekey,RSACryptoSystem,RSACryptoPublicKey,RSACryptoPrivateKey
from crypto.Mathematic import random_prime
from crypto.systems.SignatureRSA import h, SIGNATURE_BITS, RSASignatureSignerKey, RSASignatureVerifierKey, RSASignatureSystem
from crypto.template.Plaintext import Plaintext
rsa_signature = Blueprint('rsa_signature', __name__)
RSA = RSACryptoSystem()
RSA_SIG = RSASignatureSystem()

@rsa_signature.route('/genprivatekey', methods=['POST'])
def rsa_sig_genprivatekey():
    try:
        p_a = int(request.form['p_a'])
        q_a = int(request.form['q_a'])
        e_a = int(request.form['e_a'])
        if not (is_prime(p_a) and is_prime(q_a)):
            return jsonify({'error': 'Both p and q must be prime numbers.'})
        if p_a == q_a:
            return jsonify({'error': 'p_a and q_a cannot be equal.'})
        if not (isinstance(p_a, int) and isinstance(q_a, int)):
            return jsonify({'error': 'p_a and q_a must be integers.'})
        n_a, d_a= generate_RSA_privatekey(p_a, q_a, e_a)
        print(n_a, d_a)
        return jsonify({'n_a': str(n_a) , 'd_a': str(d_a)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@rsa_signature.route('/genprivatekeyb', methods=['POST'])
def rsa_sig_genprivatekeyb():
    try:
        p_b = int(request.form['p_b'])
        q_b = int(request.form['q_b'])
        e_b = int(request.form['e_b'])
        if not (is_prime(p_b) and is_prime(q_b)):
            return jsonify({'error': 'Both p and q must be prime numbers.'})
        if p_b == q_b:
            return jsonify({'error': 'p_a and q_a cannot be equal.'})
        if not (isinstance(p_b, int) and isinstance(q_b, int)):
            return jsonify({'error': 'p_a and q_a must be integers.'})
        n_b, d_b= generate_RSA_privatekey(p_b, q_b, e_b)
        print(n_b, d_b)
        return jsonify({'n_b': str(n_b) , 'd_b': str(d_b)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
    
@rsa_signature.route('/genprime', methods=['POST'])
def rsa_sig_genprime():
    try:
        if 'bits' not in request.form:
            return jsonify({'error': 'Bits not specified.'})
        if not request.form['bits'].isdigit():
            return jsonify({'error': 'Bits must be a positive integer.'})
        if int(request.form['bits']) < 1:
            return jsonify({'error': 'Bits must be a positive integer.'})
        bits = int(request.form['bits'])
        p_a = random_prime(lbound=2**bits, ubound=2 ** (bits + 1))
        q_a = random_prime(lbound=2**bits, ubound=2 ** (bits + 1))
        return jsonify({'p_a': str(p_a), 'q_a': str(q_a)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@rsa_signature.route('/genprimeee', methods=['POST'])
def rsa_sig_genprimeee():
    try:
        if 'bitse' not in request.form:
            return jsonify({'error': 'Bits not specified.'})
        if not request.form['bitse'].isdigit():
            return jsonify({'error': 'Bits must be a positive integer.'})
        if int(request.form['bitse']) < 1:
            return jsonify({'error': 'Bits must be a positive integer.'})
        bitse = int(request.form['bitse'])
        e_a = random_prime(lbound=2**bitse, ubound=2 ** (bitse + 1))
        return jsonify({'e_a': str(e_a)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@rsa_signature.route('/genprimeb', methods=['POST'])
def rsa_sig_genprimeb():
    try:
        if 'bitsb' not in request.form:
            return jsonify({'error': 'Bits not specified.'})
        if not request.form['bitsb'].isdigit():
            return jsonify({'error': 'Bits must be a positive integer.'})
        if int(request.form['bitsb']) < 1:
            return jsonify({'error': 'Bits must be a positive integer.'})
        bitsb = int(request.form['bitsb'])
        p_b = random_prime(lbound=2**bitsb, ubound=2 ** (bitsb + 1))
        q_b = random_prime(lbound=2**bitsb, ubound=2 ** (bitsb + 1))
        return jsonify({'p_b': str(p_b), 'q_b': str(q_b)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@rsa_signature.route('/genprimeeeb', methods=['POST'])
def rsa_sig_genprimeeeb():
    try:
        if 'bitsbe' not in request.form:
            return jsonify({'error': 'Bits not specified.'})
        if not request.form['bitsbe'].isdigit():
            return jsonify({'error': 'Bits must be a positive integer.'})
        if int(request.form['bitsbe']) < 1:
            return jsonify({'error': 'Bits must be a positive integer.'})
        bitsbe = int(request.form['bitsbe'])
        e_b = random_prime(lbound=2**bitsbe, ubound=2 ** (bitsbe + 1))
        return jsonify({'e_b': str(e_b)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@rsa_signature.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        m = int(request.form['m'])
        e_b = int(request.form['e_b'])
        n_b = int(request.form['n_b'])
        if m < 0 or m >= n_b:
            return jsonify({'error': 'Message m must be between 0 and n-1.'})
        public_key = RSACryptoPublicKey(n_b, e_b)
        c = RSA.encrypt(public_key, m)
        return jsonify({'c': str(c)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@rsa_signature.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        c = int(request.form['c'])
        if c < 0:
            return jsonify({'error': 'Ciphertext c must be non-negative.'})
        d_b = int(request.form['d_b'])
        n_b = int(request.form['n_b'])
        private_key = RSACryptoPrivateKey(n_b, d_b)
        m = RSA.decrypt(private_key, c)
        return jsonify({'m': str(m)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@rsa_signature.route('/signature', methods=['POST'])
def signature():
    try:
        m = int(request.form['m'])
        d_a = int(request.form['d_a'])
        n_a = int(request.form['n_a'])
        signer_key = RSASignatureSignerKey(n_a, d_a)
        sig = RSA_SIG.sign(signer_key, m)
        return jsonify({'sig': str(sig)})
    except Exception as e:
        return jsonify({'error': str(e)})

@rsa_signature.route('/verify', methods=['POST'])
def verify():
    try:
        m = int(request.form['m'])
        e_a = int(request.form['e_a'])
        n_a = int(request.form['n_a'])
        sig = int(request.form['sig'])
        verifier_key = RSASignatureVerifierKey(n_a, e_a)
        veri = RSA_SIG.verify(verifier_key, m, sig)
        return jsonify({'veri': veri})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@rsa_signature.route('/', methods=['POST'])
def convert():
    try:
        plain = request.form['plain']
        plain = RSA.str2plaintext(None, plain)
        plain = str(plain)
        return jsonify({'plain': plain})
    except Exception as e:
        return jsonify({'error': str(e)})