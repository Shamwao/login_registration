from flask_app import app
from flask import Flask
from flask import render_template, request, redirect, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return redirect('/home')

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_input(request.form):
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data= {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email" : request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = {"email" : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid Email', "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Password', "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect ('logout')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')