from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.date import Date

from flask import flash

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/find_care', methods=["POST"])
def find_care():
    if not Date.validate_create(request.form['care_date']):
        return redirect('/newappointment')
    data = {
        "care_date": request.form['care_date'],
        "provider_name": request.form['provider_name'],
        "users_id": session['user_id']
    }
    print(data)
    Date.create_one(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_date(id):
    data = {
        "id": id
    }
    Date.destroy(data)
    return redirect('/dashboard')
