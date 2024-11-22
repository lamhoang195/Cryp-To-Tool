from flask import Blueprint,request,jsonify
from flask_login import login_required
from crypto.Mathematic.is_prime import is_prime
from crypto.systems.CryptoRSA import generate_RSA_privatekey,RSACryptoSystem,RSACryptoPublicKey,RSACryptoPrivateKey
from crypto.Mathematic import random_prime
rsa = Blueprint('rsa', __name__)
rsa_signature = Blueprint('rsa_signature', __name__)
RSA = RSACryptoSystem()
@rsa.route('/genprivatekey', methods=['POST'])
def rsa_genprivatekey():
    try:
        p = int(request.form['p'])
        q = int(request.form['q'])
        e = int(request.form['e'])
        if not (is_prime(p) and is_prime(q)):
            return jsonify({'error': 'Both p and q must be prime numbers.'})
        if p == q:
            return jsonify({'error': 'p and q cannot be equal.'})
        if not (isinstance(p,int) and isinstance(q,int)):
            return jsonify({'error': 'p and q must be integers.'})
        n,d= generate_RSA_privatekey(p,q,e)
        return jsonify({'n': str(n), 'd': str(d)})
    except Exception as e:
        return jsonify({'error': str(e)})
@rsa.route('/genprime', methods=['POST'])
def rsa_genprime():
    try:
        if not request.form['bits'].isdigit():
            return jsonify({'error': 'Bits must be a positive integer.'})
        if int(request.form['bits']) < 1:
            return jsonify({'error': 'Bits must be a positive integer.'})
        bits = int(request.form['bits'])
        p = str(random_prime(lbound=2**bits, ubound=2 ** (bits + 1)))
        q = str(random_prime(lbound=2**bits, ubound=2 ** (bits + 1)))
        return jsonify({'p': p, 'q': q})
    except Exception as e:
        return jsonify({'error': str(e)})
@rsa.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        m = int(request.form['m'])
        e = int(request.form['e'])
        n = int(request.form['n'])
        if m < 0 or m >= n:
            return jsonify({'error': 'Message m must be between 0 and n-1.'})
        public_key = RSACryptoPublicKey(n, e)
        c = RSA.encrypt(public_key, m)
        return jsonify({'c': str(c)})
    except Exception as e:
        return jsonify({'error': str(e)})

@rsa.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        c = int(request.form['c'])
        if c < 0:
            return jsonify({'error': 'Ciphertext c must be non-negative.'})
        d = int(request.form['d'])
        n = int(request.form['n'])
        private_key = RSACryptoPrivateKey(n, d)
        m = RSA.decrypt(private_key, c)
        return jsonify({'m': str(m)})
    except Exception as e:
        return jsonify({'error': str(e)})
@rsa.route('/', methods=['POST'])
def convert():
    try:
        plain = request.form['plain']
        plain = RSA.str2plaintext(None, plain)
        plain = str(plain)
        return jsonify({'plain': plain})
    except Exception as e:
        return jsonify({'error': str(e)})
@rsa.route('/submit', methods=['POST'])
def submit():
    try:
        p = int(request.form['p'])
        q = int(request.form['q'])
        n = p * q
        phi_n = (p - 1) * (q - 1)
        return jsonify({'n': str(n), 'phi_n': str(phi_n)})
    except Exception as e:
        return jsonify({'error': str(e)})