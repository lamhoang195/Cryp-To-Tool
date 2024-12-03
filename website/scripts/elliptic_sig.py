from flask import Blueprint,request,jsonify
from flask_login import login_required
import random
from crypto.Mathematic import random_prime
from crypto.systems.CryptoECElGamal import ECElGamalCryptoSystem
from crypto.systems.SignatureECDSA import ECDSASignatureSystem
from crypto.elliptic_curve import EllipticCurve 
elliptic_signature = Blueprint('elliptic_signature', __name__)
ECElGamal = ECElGamalCryptoSystem()
ECElGamalSig = ECDSASignatureSystem()
@elliptic_signature.route('/genprime', methods=['POST'])
@login_required
def eliptic_signature_genprime():
    try:
        if not request.form['bits'].isdigit():
            return jsonify({'error': 'Bits must be a positive integer.'})
        if int(request.form['bits']) < 1:
            return jsonify({'error': 'Bits must be a positive integer.'})
        bits = int(request.form['bits'])
        if bits > 50:
            return jsonify({'error': 'Bits must be less than 50.'})
        p = str(random_prime(lbound=2**bits, ubound=2 ** (bits + 1)))
        return jsonify({'p': str(p)})
    except Exception as e:
     return jsonify({'error': str(e)})
@elliptic_signature.route('/encrypt', methods=['POST'])
@login_required
def eliptic_signature_encrypt():
    try:
        data = request.get_json()
        M = data.get('M') 
        p = int(data.get('p')) 
        a = int(data.get('a')) 
        b = int(data.get('b')) 
        k = int(data.get('k')) 
        P = data.get('P') 
        B = data.get('B')
        curve = EllipticCurve(p, a, b,P)
        C1,C2 = ECElGamal.encrypt(curve,B, k, M)
        print(C1,C2)
        return jsonify({'C1': C1, 'C2': C2})
    except Exception as e:
        return jsonify({'error': str(e)})
@elliptic_signature.route('/sign', methods=['POST'])
@login_required
def eliptic_signature_sign():
    try:
        data = request.get_json()
        M = data.get('M')
        p = int(data.get('p'))
        a = int(data.get('a'))
        b = int(data.get('b'))
        P = data.get('P')
        s = int(data.get('s'))

        ec = EllipticCurve(p, a, b,P)
        n = ec.num_points_on_curve
        r,S = ECElGamalSig.sign(ec,n,s, M[0])
        return jsonify({'r': r, 's': S})
    except Exception as e:
        return jsonify({'error': str(e)})
@elliptic_signature.route('/point', methods=['POST'])
@login_required
def eliptic_signature_point():
    try:
        data = request.get_json()
        p = int(data.get('p'))
        a = int(data.get('a'))
        b = int(data.get('b'))
        m = int(data.get('m'))
        P = data.get('P')
        curve = EllipticCurve(p, a, b,P)
        M = curve.get_point_by_index(m%curve.num_points_on_curve)
        return jsonify({'x': M[0], 'y': M[1]})
    except Exception as e:
        return jsonify({'error': str(e)})
