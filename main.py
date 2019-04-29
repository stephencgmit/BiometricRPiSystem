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
import arrow


client = MongoClient("mongodb://fpDBuser:project2019@fingerprintproject-shard-00-00-2ee1v.mongodb."
                     "net:27017,fingerprintproject-shard-00-01-2ee1v.mongodb.net:27017,"
                     "fingerprintproject-shard-00-02-2ee1v.mongodb.net:27017/test?ssl=true&replicaSet="
                     "FingerprintProject-shard-0&authSource=admin&retryWrites=true")

mydb = client['fingerprint_project']
students = mydb['students']
scores = mydb['scores']
log = mydb['log']

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
    session['user'] = '' # drops user session when visiting index
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
        last_login_fp = pycode.login1() # variable used to track last login fingerprint
        print('uid =' + str(last_login_fp))
        mongo_query = {"username": username}
        search = students.find(mongo_query)
        f = open("/home/pi/Desktop/FlaskTutorial/log.txt", "w")
        f.write(str(last_login_fp))
        f.close()
        #user = {'username': mongo_query['username'], 'uid': a}
        print(search)
        print(search.count()) # check number of returned usernames from mongo
        if(search.count() == 0 or last_login_fp == -1):
            print('USER NOT FOUND ')
            flash('User not found. Try Again!')
            return redirect(url_for('login'))
        else:
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_login = username + ' Logged in'
            mongo_insert = {date: log_login}
            x = log.insert_one(mongo_insert)
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
            flash('Successful Registration. You can now login')
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_register = username + ' Registered'
            mongo_insert = {date: log_register}
            x = log.insert_one(mongo_insert)
            return redirect(url_for('homepage'))
        else:
            flash('Unsuccessful Registration. You need to try again')
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
    if g.user:
        user = {'username': g.user}
        list1 = []
        for search in students.find({},{"image_template": 0, "uid":0, '_id':0}):
            if(search['username']) == user['username']:
                list1.append(search)
        print("Print the list from mongo please: " + str(list1))
        score_splitter = str(list1[0])
        new_str = score_splitter.strip('{')
        new__str = new_str.strip('}')
        new___str = new__str.replace("'", '')
        my_list = new___str.split(",")
        template = jinja_env.get_template('user.html')
        return template.render(my_list=my_list)
    flash('Login for requested page!')
    return redirect(url_for('homepage'))


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
    flash('Login for requested page!')
    return redirect(url_for('homepage'))


@app.route("/loggedin")
def loggedin():
    return render_template("login.html")


@app.route('/module/<category>', methods=["GET","POST"])
def subcategory(category):
    if g.user:
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

        elif category == "maths":
            return render_template('/modules/maths.html', user=user)
    flash('login please for access to requested page')
    return redirect(url_for('homepage'))


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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in Android quiz')
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in Cloud quiz')
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in Cpp quiz')
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in DSP quiz')
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            x = score.insert_one(mongo_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in Java quiz')
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in Javascript quiz')
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in Maths quiz')
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in Nodejs quiz')
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in Professional Engineer quiz')
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
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
            user = g.user
            date = arrow.now().format('YYYY-MM-DD hh-mm-ss')
            log_score = (user + ' scored ' + str(score) + ' in Python quiz')
            score_insert = {'uid': user, 'score1': score}
            y = scores.insert_one(score_insert)
            mongo_insert = {date: log_score}
            x = log.insert_one(mongo_insert)
            flash('Fingerprint verified. Test score submitted successfully. Stored in DB')
            flash('Check user page for all your scores')
            return redirect(url_for('score'))
        else:
            print("fingerprint not verified. Test score not submitted")
            flash('Fingerprint not verified. Test score not submitted')
            return redirect(url_for('score'))
        return render_template('user.html')


@app.route('/score')
def score():
    return render_template('score.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(password== 'admin' and username == 'admin'):
            print('hi admin')
            return redirect(url_for('viewdb'))
        else:
            print('not now admin')
            return redirect(url_for('index'))
    return render_template('admin.html')


@app.route('/admin/viewdb')
def viewdb():
    loglists = []
    for x in log.find({},{"_id":0}):
        print(x)
        loglists.append(x)
    print(loglists)
    template = jinja_env.get_template('viewdb.html')
    return template.render(loglists=loglists)



if __name__ == "__main__":
    app.run()


