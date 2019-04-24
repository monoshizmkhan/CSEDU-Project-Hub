from flask import *
import os

app = Flask(__name__)


ALLOWED_EXTENSIONS = set(['pdf', 'tex'])


@app.route('/')
def signin():
    return render_template("new.html")


@app.route('/feed')
def feed():
    '''
    posts = [{"title": "Optimization methods for large-scale machine learning",
             "authors": "L Bottou, FE Curtis, J Nocedal",
             "year": "2018",
             "field": "Machine Learning"},
            {"title": "Multi-domain connection establishment in computer networking communications",
             "authors": "Chen L, GAVRILOV C, SNAST A, Zigler",
             "year": "2018",
             "field": "Computer Networking"}]
             '''
    return render_template("feed.html", name="Saad")


@app.route('/profile')
def profile():
    prof = {"name": "Nabil Hasan",
            "session": "2014/2015",
            "mail": "nabilhasan@gmail.com",
            "contactnumber": "123123123123123",
            "research": "Natural Language Processing, Machine Learning, Artificial Intelligence",
            "picture": "static/Images/srch.png"}
    test = [{"title": "Optimization methods for large-scale machine learning",
             "authors": "L Bottou, FE Curtis, J Nocedal",
             "year": "2018",
             "abstract": "This paper provides a review and commentary on the past, present, and future of numerical optimization algorithms in the context of machine learning applications. Through case studies on text classification and the training of deep neural networks, we discuss how optimization problems arise in machine learning and what makes them challenging. A major theme of our study is that large-scale machine learning represents a distinctive setting in which the stochastic gradient (SG) method has traditionally played a central role while conventional gradient-based nonlinear optimization techniques typically falter. Based on this viewpoint, we present a comprehensive theory of a straightforward, yet versatile SG algorithm, discuss its practical behavior, and highlight opportunities for designing algorithms with improved performance. This leads to a discussion about the next generation of optimization methods for large-scale machine learning, including an investigation of two main streams of research on techniques that diminish noise in the stochastic directions and methods that make use of second-order derivative approximations.",
             "paperlink": "none",
             "githublink": "none"},
            {"title": "Understanding overlay signatures using machine learning on non-lithography context information",
             "authors": "M Overcast, C Mellegaard, D Daniel et al",
             "year": "2018",
             "abstract": "Overlay errors between two layers can be caused by non-lithography processes. While these errors can be compensated by the run-to-run system, such process and tool signatures are not always stable. In order to monitor the impact of non-lithography context on overlay at regular intervals, a systematic approach is needed. Using various machine learning techniques, significant context parameters that relate to deviating overlay signatures are automatically identified. Once the most influential context parameters are found, a run-to-run simulation is performed to see how much improvement can be obtained. The resulting analysis shows good potential for reducing the influence of hidden context parameters on overlay performance. Non-lithographic contexts are significant contributors, and their automatic detection and classification will enable the overlay roadmap, given the corresponding control capabilities.",
             "paperlink": "none",
             "githublink": "none"},
            {
                "title": "Abstractive Text Summarization using Sequence-to-sequence RNNs and Beyond",
                "authors": "Ramesh Nallapati et al",
                "year": "2016",
                "abstract": "In this work, we model abstractive text summarization using Attentional Encoder- Decoder Recurrent Neural Networks, and show that they achieve state-of-the-art performance on two different corpora. We propose several novel models that address critical problems in summarization that are not adequately modeled by the basic architecture, such as modeling key-words, capturing the hierarchy of sentence-to- word structure, and emitting words that are rare or unseen at training time. Our work shows that many of our proposed models contribute to further improvement in performance. We also propose a new dataset consisting of multi-sentence sum- maries, and establish performance bench- marks for further research.",
                "paperlink": "static/Papers/Abstractive Text Summarization using Sequence-to-sequence RNNs and Beyond.pdf",
                "githublink": "none"
            }]
    isMyProf="False"
    return render_template("profile.html", prof=prof, test=test, isMyProf=isMyProf)

'''
@app.route('/submitPaper', methods=['POST'])
def submitPaper():
    submissionRequest = request.get_json(force=True)
    title = str(submissionRequest['title'])
    authors = str(submissionRequest['authors'])
    year = str(submissionRequest['year'])
    abstract = str(submissionRequest['abstract'])
    global filepath
    addToDB = {"title": title, "authors": authors, "year": year, "abstract": abstract, "link": filepath}
    print(addToDB)
    return 'OK'
'''
@app.route('/uploadfile')
def uploadfilepage():
    return render_template('uploadfile.html')



@app.route('/search')
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

@app.route('/searchHandler', methods=['POST'])
def getSearchQuery():
    searchRequest = request.get_json(force=True)
    searchQuery = str(searchRequest['search'])
    #print(searchQuery)
    global searchTerm
    searchTerm=searchQuery
    search(searchQuery)
    return 'OK'


@app.route('/sessions')
def sessionsPage():
    return render_template('studentInfo.html')


'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

filepath=""

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file.save(app.root_path+"/static/Papers/"+filename)
        global filepath
        filepath = str(app.root_path)+"/static/Papers/"+str(filename)
        print(str(app.root_path)+"/static/Papers/"+str(filename))
    return 'OK'
'''

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

if __name__ == '__main__':
    app.run()
