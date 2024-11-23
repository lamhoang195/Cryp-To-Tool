from flask import Blueprint,request,jsonify
from flask_login import login_required
import random
elliptic = Blueprint('elliptic', __name__)

from crypto.Mathematic import random_prime
from crypto.systems.CryptoECElGamal import ECElGamalCryptoSystem
from crypto.elliptic_curve import EllipticCurve,generate_elliptic_curve_with_number_of_points_being_prime,convert_plain_number_to_point_on_curve
ECElGamal = ECElGamalCryptoSystem()
from crypto.Mathematic.bit_padding import BitPaddingConfig
RIGHT_PADDING_SIZE = 2
LEFT_PADDING_SIZE = 5
BIT_PADDING_CONFIG = BitPaddingConfig(LEFT_PADDING_SIZE, RIGHT_PADDING_SIZE)
@elliptic.route('/genprime', methods=['POST'])
def eliptic_genprime():
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
@elliptic.route('/encrypt', methods=['POST'])
@login_required
def eliptic_encrypt():
    try:
        data = request.get_json()
        M = data.get('M') 
        p = int(data.get('p')) 
        a = int(data.get('a')) 
        b = int(data.get('b')) 
        k = int(data.get('k')) 
        P = data.get('P') 
        s = int(data.get('s'))
        curve = EllipticCurve(p, a, b,P)
        B = curve.get_point_by_index(s)
        C1,C2 = ECElGamal.encrypt(curve,B, k, M)
        print(C1,C2)
        return jsonify({'C1': C1, 'C2': C2})
    except Exception as e:
        return jsonify({'error': str(e)})
@elliptic.route('/decrypt', methods=['POST'])
@login_required
def eliptic_decrypt():
    try:
        data = request.get_json()
        C1 = data.get('C1') 
        C2 = data.get('C2') 
        p = int(data.get('p')) 
        a = int(data.get('a')) 
        b = int(data.get('b')) 
        s = int(data.get('s'))
        P = data.get('P')
        curve = EllipticCurve(p, a, b,P)
        M = ECElGamal.decrypt(curve,s, C1, C2)
        return jsonify({'M': M})
    except Exception as e:
        return jsonify({'error': str(e)})