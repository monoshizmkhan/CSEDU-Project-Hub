from cseduprojecthub import APP_MAIN, APPLOGIN,Auth,DB
from flask import render_template, flash,redirect,url_for
from flask_login import current_user, login_user, logout_user , login_required
from flask import request
from models import User,load_user
from firebase_admin import auth
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from datetime import datetime
import json
from loadDB import load
import random
@APP_MAIN.route('/')
def landingPage():
    if current_user.is_authenticated:
        return redirect(url_for('FeedPage'))
    return render_template('landingPage.html', title='Home')

@APP_MAIN.route('/t')
def loaddatatodb():
    load()
    return 'asd'


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
            '''
            if(c == False):
                    return json.dumps({'status': 'You must verify email before login.'})
            '''
            print(Auth.current_user)
            login_user(User(Auth.current_user), remember=True)

            return json.dumps({'status': 'success'})
        except Exception as e:
            print(str(e))
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

@APP_MAIN.route('/uploadfile')
def uploadfilepage():
    p = current_user.get_id()
    p = p.split("'email': '")[1].split("',")[0].split('@')[0]
    a = DB.child('Users').child(p).child('Picture').get().val()

    return render_template('uploadfile.html',pic = a,id = p)


@APP_MAIN.route('/feed')
@login_required
def FeedPage():
    p = current_user.get_id()
    p = p.split("'email': '")[1].split("',")[0].split('@')[0]
    statuses = DB.child('Status').get().val()
    statid = [k for k,v in statuses.items()]
    statuses = [v for k,v in statuses.items()]
    print(statuses)
    a = DB.child('Users').child(p).child('Picture').get().val()
    b = DB.child('Users').child(p).child('Name').get().val()
    payload = []
    for i in range(len(statuses)):
        print('id',statid[i])
        pi = DB.child('Users').child(statid[i]).child('Picture').get().val()
        print("pi",pi)
        for k,v in statuses[i].items():
            payload.append(status(v['Date'], v['Name'], v['Text'],str(pi)))
    payload.reverse()
    random.shuffle(payload)
    print(statuses)
    return render_template('feed.html', title='Feed', pic = a, name = b,id = p, statuses = payload)

class status(object):

    def __init__(self,date, name,text,pic):
        self.date = date
        self.name = name
        self.text = text
        self.pic = pic

@APP_MAIN.route('/projectstatus')
@login_required
def StatusPage():
    p = current_user.get_id()
    p = p.split("'email': '")[1].split("',")[0].split('@')[0]
    statuses = DB.child('Status').child(p).get().val()
    a = DB.child('Users').child(p).child('Picture').get().val()
    b = DB.child('Users').child(p).child('Name').get().val()
    if(statuses is not None):
        statuses = [status(v['Date'], v['Name'], v['Text'], a) for k, v in statuses.items()]
    else:
        statuses = []
    print(a)
    statuses.reverse()
    return render_template('projectstatus.html', title='Feed', pic = a, name = b,id = p, statuses = statuses)

@APP_MAIN.route('/ustatus', methods=['POST'])
@login_required
def Ustatus():
    name = request.form['name']
    id = str(request.form['id'])
    text = str(request.form['text'])
    date = str(datetime.today().date())
    print(id,text,date)
    DB.child('Status').child(id).push({'Date': date, 'Name': name,
                                      'Text': text})
    print('here')
    return json.dumps({'status': 'success'})


@APP_MAIN.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@APP_MAIN.route('/profile/',defaults={'id': '#'})
@APP_MAIN.route('/profile/<string:id>')
@login_required
def profile(id):
    if (id == '#'):
        return render_template('404.html')
    print(id)
    p = DB.child('Projects').get().val()
    test = []
    for k,v in p.items():
        #print(v)
        test.append(v)
    p = current_user.get_id()
    p = p.split("'email': '")[1].split("',")[0].split('@')[0]
    print("here",p)
    isMyProf = "True"
    if(p != id):
        isMyProf = 'False'
    pic = DB.child('Users').child(p).child('Picture').get().val()
    a = DB.child('Users').child(id).get().val()
    prof = {"Name": "Nabil Hasan",
            "Session": "2014/2015",
            "Mail": "nabilhasan@gmail.com",
            "Contact": "123123123123123",
            "Research": "Natural Language Processing, Machine Learning, Artificial Intelligence",
            "Picture": "none"}


    return render_template("profile.html", pic = pic,prof=a, test=test, isMyProf=isMyProf)

@APP_MAIN.route('/upload', methods=['POST'])
def submitPaper():
    submissionRequest = request.get_json(force=True)
    title = str(submissionRequest['title'])
    authors = str(submissionRequest['authors'])
    year = str(submissionRequest['year'])
    abstract = str(submissionRequest['abstract'])
    paperlink = str(submissionRequest['paperlink'])
    githublink = str(submissionRequest['githublink'])
    if paperlink=="":
        paperlink="none"
    if githublink=="":
        githublink="none"
    addToDB = {"projectName": title, "author": authors, "year": year, "projectDescroption": abstract, "paperLink": paperlink, "githubLink": githublink}

    p = current_user.get_id()
    p = p.split("'email': '")[1].split("',")[0].split('@')[0]
    name = DB.child('Users').child(p).child('Name').get().val()
    DB.child('Status').child(p).push({'Date': str(datetime.today().date()), 'Name': name,
                                       'Text': 'I have just uploaded a project titled: '+title +
                                               '.\n Visite my profile for more details.'})
    return 'OK'


@APP_MAIN.route('/sessions')
def sessionsPage():
    return render_template('studentInfo.html')


@APP_MAIN.route('/search')
def searchResult():
    global searchTerm
    p = current_user.get_id()
    p = p.split("'email': '")[1].split("',")[0].split('@')[0]
    a = DB.child('Users').child(p).child('Picture').get().val()

    return render_template('searchresult.html', searchTerm=searchTerm,pic = a,id=p, searchResults=searchResults)

searchResults=[]
searchTerm = ""

@APP_MAIN.route('/searchHandler', methods=['POST'])
def getSearchQuery():
    searchRequest = request.get_json(force=True)
    searchQuery = str(searchRequest['search'])
    #print(searchQuery)
    global searchTerm
    searchTerm=searchQuery
    search(searchQuery)
    return 'OK'

def search(query):
    global searchResults
    searchResults.clear()
    abc = str(query).upper()
    query = abc
    p = DB.child('Projects').get().val()
    projects = []
    print(p)
    for k, v in p.items():
        print(k,v)
        projects.append(v)
    print('pro',projects)
    #projects naam er list of dictionaries, should contain a dictionary each for a project
    for i in projects:
        if ((str(i['projectName'])).upper()).__contains__(query) or ((str(i['author'])).upper()).__contains__(query):
            temp=i
            if temp not in searchResults:
                searchResults.append(temp)
    print('sear',searchResults)

