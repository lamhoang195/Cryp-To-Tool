from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if len(name) < 3:
            flash('Name must be greater than 3 characters.', category='error')
        elif len(email) < 4:
            flash('Mail must be greater than 3 character.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password != confirm_password:
            flash('Password and Confirm password must be the same.', category='error')
        else:
            flash('Account created!', category='success')
            
    return render_template("signup.html")

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    data = request.form
    print(data)
    return render_template("signin.html")

@auth.route('/logout')
def logout():
    return "<h1>Hello Logout</h1>"

