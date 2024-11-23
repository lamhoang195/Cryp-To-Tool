from flask import Blueprint, render_template,request,flash,jsonify
from flask_login import login_required
import math
elgamal = Blueprint('elgamal', __name__)
elgamal_signature = Blueprint('elgamal_signature', __name__)
from crypto.systems.CryptoElGamal import ElGamalCryptoSystem,ElGamalCryptoPublicKey,ElGamalCryptoPrivateKey,ElGamal_generate_keypair
from crypto.Mathematic import is_prime,random_prime
ElGamal = ElGamalCryptoSystem()
@elgamal.route('/genkey', methods=['POST'])
def genkey():
    try:
        p = int(request.form['p'])
        alpha = int(request.form['alpha'])
        a = int(request.form['a'])
        if not (is_prime(p)):
            return jsonify({'error': ' p  must be prime numbers.'})
        if not (isinstance(p,int) and isinstance(alpha,int)):
            return jsonify({'error': 'p and alpha must be integers.'})
        if a >= p:
            return jsonify({'error': 'a must be less than p.'})
        beta = ElGamal_generate_keypair(p)[0][2]
        return jsonify({'beta': str(beta)})
    except Exception as e:
        return jsonify({'error': str(e)})
@elgamal.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        m = int(request.form['m'])
        p = int(request.form['p'])
        alpha = int(request.form['alpha'])
        beta = int(request.form['beta'])
        k = int(request.form['k'])
        if m < 0 or m >= p:
            return jsonify({'error': 'Message m must be between 0 and p-1.'})
        if not (is_prime(p) and is_prime(alpha)):
            return jsonify({'error': 'Both p and g must be prime numbers.'})
        if not (isinstance(p,int) and isinstance(alpha,int)):
            return jsonify({'error': 'p and g must be integers.'})
        c1,c2 = ElGamal.encrypt(ElGamalCryptoPublicKey(p, alpha, beta),k, m)
        return jsonify({'c1': str(c1)   , 'c2': str(c2)})
    except Exception as e:
        return jsonify({'error': str(e)})
@elgamal.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        c1 = int(request.form['c1'])
        c2 = int(request.form['c2'])
        p = int(request.form['p'])
        a = int(request.form['a'])
        if not (is_prime(p)):
            return jsonify({'error': 'p must be a prime number.'})
        if not (isinstance(p,int)):
            return jsonify({'error': 'p must be an integer.'})
        m = ElGamal.decrypt(ElGamalCryptoPrivateKey(p, a), [c1, c2])
        return jsonify({'m': str(m)})
    except Exception as e:
        return jsonify({'error': str(e)})
@elgamal.route('/genprime', methods=['POST'])
def genprime():
    try:
        if not request.form['bits'].isdigit():
            return jsonify({'error': 'Bits must be a positive integer.'})
        if int(request.form['bits']) < 1:
            return jsonify({'error': 'Bits must be a positive integer.'})
        bits = int(request.form['bits'])
        p = str(random_prime(lbound=2**bits, ubound=2 ** (bits + 1)))
        return jsonify({'p': p})
    except Exception as e:
        return jsonify({'error': str(e)})
@elgamal.route('/', methods=['POST'])
def convert():
    try:
        plain = request.form['plain']
        plain = ElGamal.str2plaintext(None, plain)
        plain = str(plain)
        return jsonify({'plain': plain})
    except Exception as e:
        return jsonify({'error': str(e)})
@elgamal.route('/genalpha', methods=['POST'])
def genalpha():
    try:
        p = int(request.form['p'])
        if not is_prime(p):
            return jsonify({'error': 'p must be a prime number.'})
        if not isinstance(p,int):
            return jsonify({'error': 'p must be an integer.'})
        alpha = ElGamal_generate_keypair(p)[0][1]
        return jsonify({'alpha': str(alpha)})
    except Exception as e:
        return jsonify({'error': str(e)})