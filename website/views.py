from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/home')
def home():
    return render_template("index.html")

@views.route('/rsa')
def rsa():
    return render_template("rsa.html")

@views.route('/elgamal')
def elgamal():
    return render_template("elgamal.html")

@views.route('/elliptic')
def elliptic():
    return render_template("elliptic.html")

@views.route('/rsa__signature')
def rsa_signature():
    return render_template("rsa_signature.html")

@views.route('/elgamal_signature')
def elgamal_signature():
    return render_template("elgamal_signature.html")

@views.route('/elliptic_signature')
def elliptic_signature():
    return render_template("elliptic_signature.html")