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

@APP_MAIN.route('/uploadfile')
def uploadfilepage():
    return render_template('uploadfile.html')


@APP_MAIN.route('/feed')
@login_required
def FeedPage():
    statuses = [status() for i in range(10)]
    return render_template('feed.html', title='Feed', name = "Saad", statuses = statuses)

class status(object):

    def __init__(self,):
        self.date = datetime.today()
        self.text = "This is a test."

@APP_MAIN.route('/projectstatus')
@login_required
def StatusPage():
    statuses = [status() for i in range(10)]
    return render_template('projectstatus.html', title='Feed', name = "Saad", statuses = statuses)

@APP_MAIN.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@APP_MAIN.route('/profile')
def profile():
    prof = {"name": "Dr. L Bottou", "designation": "Professor", "mail": "lbottou@mail.com", "contactnumber": "123123123123123", "research": "Machine Learning, Artificial Intelligence"}
    test = [{"title": "Optimization methods for large-scale machine learning",
             "authors": "L Bottou, FE Curtis, J Nocedal",
             "year": "2018",
             "abstract": "This paper provides a review and commentary on the past, present, and future of numerical optimization algorithms in the context of machine learning applications. Through case studies on text classification and the training of deep neural networks, we discuss how optimization problems arise in machine learning and what makes them challenging. A major theme of our study is that large-scale machine learning represents a distinctive setting in which the stochastic gradient (SG) method has traditionally played a central role while conventional gradient-based nonlinear optimization techniques typically falter. Based on this viewpoint, we present a comprehensive theory of a straightforward, yet versatile SG algorithm, discuss its practical behavior, and highlight opportunities for designing algorithms with improved performance. This leads to a discussion about the next generation of optimization methods for large-scale machine learning, including an investigation of two main streams of research on techniques that diminish noise in the stochastic directions and methods that make use of second-order derivative approximations.",
             "link": "none"},
            {"title": "Understanding overlay signatures using machine learning on non-lithography context information",
             "authors": "M Overcast, C Mellegaard, D Daniel et al",
             "year": "2018",
             "abstract": "Overlay errors between two layers can be caused by non-lithography processes. While these errors can be compensated by the run-to-run system, such process and tool signatures are not always stable. In order to monitor the impact of non-lithography context on overlay at regular intervals, a systematic approach is needed. Using various machine learning techniques, significant context parameters that relate to deviating overlay signatures are automatically identified. Once the most influential context parameters are found, a run-to-run simulation is performed to see how much improvement can be obtained. The resulting analysis shows good potential for reducing the influence of hidden context parameters on overlay performance. Non-lithographic contexts are significant contributors, and their automatic detection and classification will enable the overlay roadmap, given the corresponding control capabilities.",
             "link": "none"},
            {
                "title": "Abstractive Text Summarization using Sequence-to-sequence RNNs and Beyond",
                "authors": "Ramesh Nallapati et al",
                "year": "2016",
                "abstract": "In this work, we model abstractive text summarization using Attentional Encoder- Decoder Recurrent Neural Networks, and show that they achieve state-of-the-art performance on two different corpora. We propose several novel models that address critical problems in summarization that are not adequately modeled by the basic architecture, such as modeling key-words, capturing the hierarchy of sentence-to- word structure, and emitting words that are rare or unseen at training time. Our work shows that many of our proposed models contribute to further improvement in performance. We also propose a new dataset consisting of multi-sentence sum- maries, and establish performance bench- marks for further research.",
                "link": "static/Papers/Abstractive Text Summarization using Sequence-to-sequence RNNs and Beyond.pdf"
            }]
    return render_template("profile.html", prof=prof, test=test)


@APP_MAIN.route('/search')
def searchResult():
    global searchTerm
    return render_template('searchresult.html', searchTerm=searchTerm, searchResults=searchResults)

searchResults=[]
searchTerm = ""
prof = [{"name": "Dr. L Bottou", "designation": "Professor", "mail": "lbottou@mail.com", "contactnumber": "123123123123123", "research": "Machine Learning, Artificial Intelligence"}]
test = [{"title": "Optimization methods for large-scale machine learning",
             "authors": "L Bottou, FE Curtis, J Nocedal",
             "year": "2018",
             "abstract": "This paper provides a review and commentary on the past, present, and future of numerical optimization algorithms in the context of machine learning applications. Through case studies on text classification and the training of deep neural networks, we discuss how optimization problems arise in machine learning and what makes them challenging. A major theme of our study is that large-scale machine learning represents a distinctive setting in which the stochastic gradient (SG) method has traditionally played a central role while conventional gradient-based nonlinear optimization techniques typically falter. Based on this viewpoint, we present a comprehensive theory of a straightforward, yet versatile SG algorithm, discuss its practical behavior, and highlight opportunities for designing algorithms with improved performance. This leads to a discussion about the next generation of optimization methods for large-scale machine learning, including an investigation of two main streams of research on techniques that diminish noise in the stochastic directions and methods that make use of second-order derivative approximations."},
        {"title": "Optimization methods for large-scale machine learning",
             "authors": "L Bottou, FE Curtis, J Nocedal",
             "year": "2018",
             "abstract": "This paper provides a review and commentary on the past, present, and future of numerical optimization algorithms in the context of machine learning applications. Through case studies on text classification and the training of deep neural networks, we discuss how optimization problems arise in machine learning and what makes them challenging. A major theme of our study is that large-scale machine learning represents a distinctive setting in which the stochastic gradient (SG) method has traditionally played a central role while conventional gradient-based nonlinear optimization techniques typically falter. Based on this viewpoint, we present a comprehensive theory of a straightforward, yet versatile SG algorithm, discuss its practical behavior, and highlight opportunities for designing algorithms with improved performance. This leads to a discussion about the next generation of optimization methods for large-scale machine learning, including an investigation of two main streams of research on techniques that diminish noise in the stochastic directions and methods that make use of second-order derivative approximations."},
            {"title": "Understanding overlay signatures using machine learning on non-lithography context information",
             "authors": "M Overcast, C Mellegaard, D Daniel et al",
             "year": "2018",
             "abstract": "Overlay errors between two layers can be caused by non-lithography processes. While these errors can be compensated by the run-to-run system, such process and tool signatures are not always stable. In order to monitor the impact of non-lithography context on overlay at regular intervals, a systematic approach is needed. Using various machine learning techniques, significant context parameters that relate to deviating overlay signatures are automatically identified. Once the most influential context parameters are found, a run-to-run simulation is performed to see how much improvement can be obtained. The resulting analysis shows good potential for reducing the influence of hidden context parameters on overlay performance. Non-lithographic contexts are significant contributors, and their automatic detection and classification will enable the overlay roadmap, given the corresponding control capabilities."}]

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
    #print(query)
    for i in prof:
        if (str(i['name']).upper()).__contains__(query) or ((str(i['research'])).upper()).__contains__(query):
            temp=i
            temp['type']='prof'
            #print(temp)
            if temp not in searchResults:
                searchResults.append(temp)
    for i in test:
        if ((str(i['title'])).upper()).__contains__(query) or ((str(i['authors'])).upper()).__contains__(query):
            temp=i
            temp['type']='work'
            if temp not in searchResults:
                searchResults.append(temp)
    print(searchResults)

'''
<!--
              {% for status in statuses %}
                    {% if loop.index == 0 %}
                        <div class="carousel-item active">
                            <img class="d-block w-100" src="/static/Images/images.jpeg" alt="First slide">
                            <div class="carousel-caption d-none d-md-block">
                                {% include 'statusview.html' %}
                            </div>
                        </div>
                    {% else %}
                        <div class="carousel-item">
                            <img class="d-block w-100" src="/static/Images/images.jpeg" alt="Other slide">
                            <div class="carousel-caption d-none d-md-block">
                                {% include 'statusview.html' %}
                            </div>
                        </div>
                    {% endif %}
              {% endfor %}
              -->
'''