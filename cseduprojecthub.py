import os
from flask import Flask
import firebase_admin
from firebase_admin import credentials
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import pyrebase
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

config = {
    "apiKey": "AIzaSyCDTuoTD4XDdHpocCIUtJ8MoegvhHDGY_0",
    "authDomain": "cseduprojecthub.firebaseapp.com",
    "databaseURL": "https://cseduprojecthub.firebaseio.com",
    "projectId": "cseduprojecthub",
    "storageBucket": "cseduprojecthub.appspot.com",
    "messagingSenderId": "1011227060317"
}

APP_MAIN = Flask(__name__)
APP_MAIN.config.from_object(Config)
APPBS=Bootstrap(APP_MAIN)
APPLOGIN = LoginManager(APP_MAIN)
APPLOGIN.login_view = 'login'
firebase = pyrebase.initialize_app(config)
Auth = firebase.auth()
DB = firebase.database()
cred = credentials.Certificate('static/key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cseduprojecthub.firebaseio.com'
})
import routes,models,errors


