from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def present_login():
    return render_template('index.html')

# More routes can go here.