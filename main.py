from flask import Flask, render_template, flash, request, url_for, redirect
#from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, current_user
import json
from pymongo import MongoClient
import time
from random import shuffle
from pyfingerprint import *
import pycode 


client = MongoClient("mongodb://fpDBuser:project2019@fingerprintproject-shard-00-00-2ee1v.mongodb."
                     "net:27017,fingerprintproject-shard-00-01-2ee1v.mongodb.net:27017,"
                     "fingerprintproject-shard-00-02-2ee1v.mongodb.net:27017/test?ssl=true&replicaSet="
                     "FingerprintProject-shard-0&authSource=admin&retryWrites=true")

mydb = client['fingerprint_project']
connect_to_collection = mydb['students']

app = Flask(__name__)

@app.route("/")
def home():
    #flash("Hellooooooooo")
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
        key = request.form['username']
        print(key)
        a = pycode.login()
        print(a)
        if request.form['username'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('dashboard'))

    return render_template('login_template.html', error=error)


@app.route("/")
@app.route("/homepage")
def homepage(user=None):
    return render_template("homepage.html", user=user)


@app.route("/")
@app.route("/register/", methods=['GET','POST'])
def register(user=None): 
    if request.method == 'POST':
        key = request.form['username']
        print(key)
        a = pycode.login()
        print(a)
        if request.form['username'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('dashboard'))
    return render_template("register.html", user=user)


@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/")
@app.route("/user")
def user():
    return render_template("user.html")


@app.route("/")
@app.route("/loggedin")
def loggedin():
    return render_template("loggedin.html")




@app.route('/')
@app.route('/module/<category>', methods=["GET","POST"])
def subcategory(category):
    if category == "java":
        return render_template('java.html')

    elif category == "android":
        if request.method == 'POST':
            num = request.form['score']
            print(type(num))
            print(num)
        return render_template('android.html')

    elif category == "cpp":
        return render_template('cpp.html')

    elif category == "cloud":
        return render_template('cloud.html')

    elif category == "proeng":
        return render_template('profeng.html')

    elif category == "dsp":
        return render_template('dsp.html')

    elif category == "python":
        return render_template('python.html')

    elif category == "javascript":
        return render_template('javascript.html')

    elif category == "nodejs":
        return render_template('nodejs.html')

    elif category == "math":
        return render_template('math.html')




if __name__ == "__main__":
    app.run()


