from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        

        user = User.query.filter_by(email=email).first()
        if user: 
            flash('Email already exists.', category='error')
        elif len(name) < 3:
            flash('Name must be greater than 3 characters.', category='error')
        elif len(email) < 4:
            flash('Mail must be greater than 3 character.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password != confirm_password:
            flash('Password and Confirm password must be the same.', category='error')
        else:
            new_user = User(name=name, email=email, password=generate_password_hash(
                password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            flash('Account created!', category='success')
            return redirect(url_for('auth.signup'))
    return render_template("signup.html", user=current_user)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Signed in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("signin.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.signin'))

