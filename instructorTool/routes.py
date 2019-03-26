from flask import render_template, url_for, json, flash, redirect, request
from instructorTool import app
from instructorTool.forms import LoginForm
from instructorTool.Canvas_Scripts.canvas_calendar import Canvas_Calendar
import json
from instructorTool.models import User, Configuration
from instructorTool import db, login_manager
import requests 
from flask_login import login_user, current_user, logout_user, login_required
from flask import jsonify, session
import jwt
import base64
import json

course = '15760'
canvas_token = '7236~UoRqWAyLYPwM3ArUdvszjsidpNisiFq2N4XnlMFIr3Uh3TNOVuhP7qv05awogom2'

with open('instructorTool/courseslist.json') as f:
        courses = json.load(f)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title ="Home",courses= courses)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/cal")
def cal():
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.getallevents(course)
    print(result['assignments'])
    myevents = json.dumps(result['events'])
    assignments = json.dumps(result['assignments'])
    return render_template('calendar.html', events = myevents, assignments = assignments, course= "course_"+course)

@app.route("/newevent", methods=['POST'])
def newEvents():
    response = request.data
    responseObj = json.loads(response)
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.create_event(responseObj)
    return result

@app.route("/editevent", methods=['POST'])
def editEvents():
    response = request.data
    responseObj = json.loads(response)
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.edit_event(responseObj)
    return result

@app.route("/deleteevent", methods=['POST'])
def deleteEvents():
    response = request.data
    responseObj = json.loads(response)
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.delete_event(responseObj)
    return result

@app.route("/editassign", methods=['POST'])
def editAssign():
    response = request.data
    responseObj = json.loads(response)
    print(responseObj)
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.edit_assignment(responseObj, course)
    return result

@app.route('/send', methods=['GET','POST'])
def send():
    if request.method== 'POST':
        return render_template('coursepage.html',title = "Course Page")

    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
#@login_required
def account():
    return render_template('account.html')

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

@app.route("/google")
def sendrequest():
    client_id = Configuration.query.filter_by(key="oauth_client_id").first().value
    url = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id="\
    + str(client_id)\
    +"&scope=https://www.googleapis.com/auth/spreadsheets+https://www.googleapis.com/auth/drive.file+https://www.googleapis.com/auth/drive+email+profile&redirect_uri=http://127.0.0.1:5000/oauthcallback"
    return redirect(url)

@app.route("/initconfig")
def initdatabase():
    return render_template('initconfig.html')

@app.route("/addconfig")
def addconfig():
    name = request.args.get('name')
    value = request.args.get('value')
    config = Configuration.query.filter_by(key=name).first()
    if config:
        config.value = value
        db.session.flush()
        db.session.commit()
        return ("Configuration updated successfully")
    else:
        config = Configuration(name, value)
        db.session.add(config)
        db.session.commit()
    return ("Configuration added successfully")

