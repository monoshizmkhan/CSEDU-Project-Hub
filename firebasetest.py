import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
from firebase import firebase

import os
cred = credentials.Certificate('static/key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cseduprojecthub.firebaseio.com'
})

ref = db.reference('/')
users_ref = ref.child('tusers')
users_ref.set({
    'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})
print(
    users_ref.push({
    'palanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    }}).key)
'''
user = auth.create_user(
    email='saadmahmud14@example.com',
    email_verified=False,
    phone_number='+15555550100',
    password='asdasd',
    display_name='John Doe',
    photo_url='http://www.example.com/12345678/photo.png',
    disabled=True)
print('Sucessfully created new user: {0}'.format(user.uid))
'''
email = 'saadmahmud14@example.com'
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
'''
message = Mail(
    from_email='cseduprojecthub@example.com',
    to_emails='saadmahmud14@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(str(e))
'''
