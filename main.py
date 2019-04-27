from flask import Flask, render_template, flash, request, url_for, redirect, session, g
#from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, current_user
import json
from pymongo import MongoClient
import time
from random import shuffle
import jinja2
import os
from flask_login import LoginManager, UserMixin
from flask_login import current_user, login_user
from pyfingerprint import *
import pycode 


client = MongoClient("mongodb://fpDBuser:project2019@fingerprintproject-shard-00-00-2ee1v.mongodb."
                     "net:27017,fingerprintproject-shard-00-01-2ee1v.mongodb.net:27017,"
                     "fingerprintproject-shard-00-02-2ee1v.mongodb.net:27017/test?ssl=true&replicaSet="
                     "FingerprintProject-shard-0&authSource=admin&retryWrites=true")

mydb = client['fingerprint_project']
students = mydb['students']
scores = mydb['scores']

app = Flask(__name__)

app.secret_key = os.urandom(24)     # generate random string to encrypt cookie and decrypt

template_dir = os.path.join(os.path.dirname("__file__"), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

user = {}
items = []
position_number = 0
global last_login_fp
last_login_fp = 0

@app.route("/")
def home():
    #flash("Hellooooooooo")
    session['user'] = ''
    return render_template("homepage.html")

# Route for handling the login page logic
# @app.route('/login')
# def login_template():
#     #flash("Hellooooooooo")
#     return render_template("login_template.html")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session.pop('user', None)
        username=request.form['username']
        print(username)
        session['user'] = request.form['username']
        last_login_fp = pycode.login() # variable used to track last login fingerprint
        print('uid =' + str(last_login_fp))
        mongo_query = {"username": username}
        search = students.find(mongo_query)
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "w")
        f.write(str(last_login_fp))
        f.close()
        #user = {'username': mongo_query['username'], 'uid': a}
        print(search)
        print(search.count()) # check number of returned usernames from mongo
        if(search.count() == 0):
            print('USER NOT FOUND IN MONGODB')
            #flash('user not found')
            return redirect(url_for('homepage'))
        else:
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)


@app.route("/homepage")
def homepage(user=None):
    session['user'] = ''
    return render_template("homepage.html")


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route("/register/", methods=['GET','POST'])
def register(): 
    if request.method == 'POST':
        uname = request.form['username']
        print(uname)
        a = pycode.reg(uname)
        print(a)
        if a == 1:
            print("successful registration")
        else:
            return redirect(url_for('register'))
    return render_template("register.html")



@app.route("/download_fingerprint/", methods=['GET', 'POST'])
def download_fingerprint():
    if request.method == 'POST':
        uname = request.form['un']
        pycode.upload_fingerprint_template(uname)
        return render_template("homepage.html")
    return render_template("downloadtemp.html")

#@app.route("/profile/")
#def profile():
#    if g.user:
#        print(g.user)
#        user = {'username': g.user}
#        print(user)
#        return render_template("user.html", user=user)
#    return redirect(url_for('homepage'))


@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'Not Logged in'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return 'Dropped!'

@app.route("/")
@app.route("/dashboard")
def dashboard():
    user = {'username': g.user}
    return render_template("dashboard.html", user=user)


@app.route("/user")
def user():
    user = {'username': g.user}
    list1 = []
    for search in students.find({},{"image_template": 0, "uid":0, '_id':0}):
        if(search['username']) == user['username']:
            list1.append(search)
    score_splitter = str(list1[0])
    new_str = score_splitter.strip('{')
    new__str = new_str.strip('}')
    new___str = new__str.replace("'", '')
    my_list = new___str.split(",")
    template = jinja_env.get_template('user.html')
    return template.render(my_list=my_list)

@app.route("/leaderboard")# using jinja templating to render scores from mongo
def leaderboard():
    if g.user:
        user = {'username': g.user}
        items = []
        print(user)
        for x in scores.find({}, {"_id": 0}).sort("score1", -1):
            print(x)
            items.append(x)
        #items = dict(zip(doc[::2],doc[1::2]))
        template = jinja_env.get_template('leaderboard.html')
        return template.render(items=items, user=user)
    return render_template("homepage.html")


@app.route("/loggedin")
def loggedin():
    return render_template("login.html")


@app.route('/module/<category>', methods=["GET","POST"])
def subcategory(category):
    user = {'username': g.user}
    if category == "java":
        return render_template('/modules/java.html', user=user)

    elif category == "android":
        return render_template('/modules/android.html', user=user)

    elif category == "cpp":
        return render_template('/modules/cpp.html', user=user)

    elif category == "cloud":
        return render_template('/modules/cloud.html' , user=user)

    elif category == "proeng":
        return render_template('/modules/profeng.html',user=user)

    elif category == "dsp":
        return render_template('/modules/dsp.html', user=user)

    elif category == "python":
        return render_template('/modules/python.html', user=user)

    elif category == "javascript":
        return render_template('/modules/javascript.html', user=user)

    elif category == "nodejs":
        return render_template('/modules/nodejs.html', user=user)

    elif category == "math":
        return render_template('/modules/maths.html', user=user)


@app.route('/android/<score_id>', methods=['GET', 'POST'])
def score1(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'android':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')

@app.route('/cloud/<score_id>', methods=['GET', 'POST'])
def score2(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'cloud':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')


@app.route('/cpp/<score_id>', methods=['GET', 'POST'])
def score3(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'cpp':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')


@app.route('/dsp/<score_id>', methods=['GET', 'POST'])
def score4(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'dsp':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')


@app.route('/java/<score_id>', methods=['GET', 'POST'])
def score5(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'java':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')


@app.route('/javascript/<score_id>', methods=['GET', 'POST'])
def score6(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'javascript':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')


@app.route('/maths/<score_id>', methods=['GET', 'POST'])
def score7(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'maths':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')


@app.route('/nodejs/<score_id>', methods=['GET', 'POST'])
def score8(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'nodejs':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')


@app.route('/proeng/<score_id>', methods=['GET', 'POST'])
def score9(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'proeng':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')


@app.route('/python/<score_id>', methods=['GET', 'POST'])
def score10(score_id):
    user = {'username': g.user}
    if request.method == 'GET':
        score = int(score_id)
        score = score*10
        print("Users score is: " + str(score))
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "r")
        last_login_fp = f.readline()
        print(last_login_fp)
        verify = pycode.verify_test()
        print("verify = " + str(verify))
        print("last_login_fp = " + str(last_login_fp))
        if (str(verify) == last_login_fp):
            print("fingerprint verified")
            students.find_one_and_update({"username": g.user}, {"$set": {'python':score}})
            return redirect(url_for('user'))
        else:
            print("fingerprint not verified. Restart Quiz Please")
            return redirect(url_for('user'))
        return render_template('user.html')



if __name__ == "__main__":
    app.run()


