from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return redirect(url_for('auth.signin'))

@views.route('/home')
def home():
    return render_template("index.html")
@views.route('/rsa')
@login_required
def rsa():
    return render_template("rsa.html")
@views.route('/elgamal')
@login_required
def elgamal():
    return render_template("elgamal.html")

@views.route('/elliptic')
@login_required
def elliptic():
    return render_template("elliptic.html")

@views.route('/rsa_signature')
@login_required
def rsa_signature():
    return render_template("rsa_signature.html")

@views.route('/elgamal_signature')
@login_required
def elgamal_signature():
    return render_template("elgamal_signature.html")

@views.route('/elliptic_signature')
@login_required
def elliptic_signature():
    return render_template("elliptic_signature.html")
@views.route('/contact')
def contact():
    return render_template("contact.html")