from flask import Blueprint,request,jsonify
from flask_login import login_required
import random
elliptic = Blueprint('elliptic', __name__)
elliptic_signature = Blueprint('elliptic_signature', __name__)
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
@elliptic_signature.route('/genprime', methods=['POST'])
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
