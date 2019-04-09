from cseduprojecthub import APP_MAIN, APPLOGIN,Auth,DB
from flask import render_template, flash,redirect,url_for,abort
from flask_login import current_user, login_user, logout_user , login_required
from flask import request
from models import User
from firebase_admin import auth
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from datetime import datetime
import json

@APP_MAIN.route('/')
def landingPage():
    return render_template('landingPage.html', title='Home')


@APP_MAIN.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('FeedPage'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        print(email)
        print(password)
        try:
            Auth.sign_in_with_email_and_password(email, password)
            c = Auth.get_account_info(Auth.current_user['idToken'])['users'][0]['emailVerified']
            if(c == False):
                    return json.dumps({'status': 'You must verify email before login.'})
            login_user(User(Auth.current_user), remember=True)
            return json.dumps({'status': 'success'})
        except Exception as e:
            return json.dumps({'status': 'Something went wrong! Try again.'})
    return render_template('login.html', title='Login')


@APP_MAIN.route('/register',methods=['GET', 'POST'])
def RagisterPage():
    if request.method == 'POST':
        try:
            auth.create_user(
                email=request.form['email']+'@students.cse.du.ac.bd',
                email_verified=False,
                password=request.form['pass'],
                display_name=request.form['fname']+request.form['lname'],
                disabled=False)
            Auth.send_email_verification(request.form['email']+'@students.cse.du.ac.bd')
            return json.dumps({'status': 'success'})
        except Exception as e:
            return json.dumps({'status': 'Something went wrong! Try again.'})
    return render_template('register.html', title='Register')

@APP_MAIN.route('/fpv',methods=['GET', 'POST'])
def fpv():
    if request.method == 'POST':
        email = request.form['email']
        tp = request.form['tp']
        try:
            if(tp == 'r'):
                Auth.send_password_reset_email(email)
            else:
                Auth.send_email_verification(email)
            return json.dumps({'status': 'success'})
        except Exception as e:
            flash('Something went wrong!! Please check input.')
            return json.dumps({'status': str(e)})
    else:
        return render_template('forv.html', title='Forgot Password')

@APP_MAIN.route('/feed')
@login_required
def FeedPage():
    return render_template('feed.html', title='Feed', name = "Saad")

@APP_MAIN.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))