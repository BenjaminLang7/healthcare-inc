from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def present_login():
    return render_template('index.html')

@app.route('/register_user', methods=["POST"])
def register():
    if not User.validate_account(request.form):
        return redirect('/')
    encrypted_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "insurance": request.form['insurance'],
        "password": encrypted_pw,
    }
    User.register(data)
    return redirect('/dashboard')


@app.route('/login_user', methods=["POST"])
def login():
    data = {
        "email": request.form['email']
    }
    user_with_email = User.get_user_by_email(data)
    if user_with_email == False:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_with_email.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_with_email.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    one_user = User.get_user_by_id(data)
    user_list = User.get_all(data)
    print(user_list)
    return render_template('dashboard.html', current_user = one_user, all_users = user_list)


# if we create a logout button

#@app.route('/logout')
#def logout():
    #session.clear()
    #return redirect('/')