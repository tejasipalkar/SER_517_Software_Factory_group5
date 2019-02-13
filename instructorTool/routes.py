from flask import render_template, url_for, flash, redirect, request
from instructorTool import app
from instructorTool.forms import LoginForm
from instructorTool.models import User, Configuration
from instructorTool import db, login_manager

from flask_login import login_user, current_user, logout_user, login_required
import requests 
from flask import jsonify, session
import jwt
import base64
import json



#if logged-in only then take user to home page and show list of courses
# else redirect user to login page and show alert that they need to log in first



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/course")
def course():
    return render_template('course.html')


@app.route("/document")
def fetch_document():
    doc_id = request.args.get('doc_id')
    access_token = session['access_token']
    r=requests.get("https://www.googleapis.com/drive/v3/files/"+doc_id+"/export?mimeType=text/csv", headers={"Authorization":access_token})
    return r.text


@app.route("/oauthcallback")
def callback():
    code = request.args.get('code')
    client_id = Configuration.query.filter_by(key="oauth_client_id").first().value
    client_secret = Configuration.query.filter_by(key="oauth_client_secret").first().value
    PARAMS = {'code':code, 'client_id': client_id, 
    'client_secret': client_secret, 'redirect_uri': 'http://127.0.0.1:5000/oauthcallback',
    'grant_type': 'authorization_code'} 
    URL = "https://oauth2.googleapis.com/token"
    # sending get request and saving the response as response object 
    r = requests.post(url = URL, data = PARAMS) 
    # extracting data in json format 
    data = r.json() 
    segments = data['id_token'].split('.')

    if (len(segments) != 3): 
        raise Exception('Wrong number of segments in token: %s' % id_token) 

    b64string = segments[1]
    padding =  '=' * (4 - len(b64string) % 4) 
    padded = str(b64string) + str(padding)
    response = base64.b64decode(padded)
    response = str(response, 'utf-8')
    res = json.loads(response)
    email = res['email']
    name = res['name']
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
    else:
        user = User(name, email)
        db.session.add(user)
        db.session.commit()
        login_user(user)
    access_token = data['access_token']
    access_token = "Bearer " + access_token
    session['access_token'] = access_token
    return redirect(url_for('account'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (user.password == form.password.data):
                login_user(user, remember=form.remember.data)
                flash(format('Login Successful. Welcome!'), 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(format('Login Unsuccessful. Please check username and password!'), 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html')