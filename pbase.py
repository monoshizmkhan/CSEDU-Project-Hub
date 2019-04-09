import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
from flask import *
app = Flask(__name__)
config = {
    "apiKey": "AIzaSyCDTuoTD4XDdHpocCIUtJ8MoegvhHDGY_0",
    "authDomain": "cseduprojecthub.firebaseapp.com",
    "databaseURL": "https://cseduprojecthub.firebaseio.com",
    "projectId": "cseduprojecthub",
    "storageBucket": "cseduprojecthub.appspot.com",
    "messagingSenderId": "1011227060317"
}
firebase = pyrebase.initialize_app(config)

A = firebase.auth()

db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def basic():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'

    if(A.current_user is not None):
        print(A.current_user)
        return render_template('new.html', s=successful)
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        print(db.child('auth').child(email[:-4]).get().val())
        try:
            A.sign_in_with_email_and_password(email, password)
            return render_template('new.html', s=successful)
        except:
            return render_template('new.html', us=unsuccessful)

    return render_template('new.html')

print("here")
if (__name__ == 'pbase'):
    db.child("auth").child("saadmahmud14@gmail").set(1)
    db.child("auth").child("saadmahmud14@example").set(0)
    A.current_user = None
    user = A.sign_in_with_email_and_password("saadmahmud14@example.com","asdasd")
    print(user)
    print(A.get_account_info(user['idToken']))
    try:
        print("here")
        '''
        user = auth.create_user(
            email='saadmahmud14@gmail.com',
            email_verified=False,
            phone_number='+15555550109',
            password='asdasd',
            display_name='John Doe',
            photo_url='http://www.example.com/12345678/photo.png',
            disabled=False)
        print('Sucessfully created new user: {0}'.format(user.uid))
        '''
        #user = A.sign_in_with_email_and_password('saadmahmud14@gmail.com',"asdasd")
        #A.send_email_verification(user['idToken'])
        print(A.current_user)
        #A.get_account_info(user['idToken'])
        print(A.current_user)
        #app.run()
    except Exception as e:
        print(str(e))
