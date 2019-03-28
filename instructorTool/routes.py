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
import csv
import pandas as pd
import traceback
import sys

course = '15760'
canvas_token = '7236~UoRqWAyLYPwM3ArUdvszjsidpNisiFq2N4XnlMFIr3Uh3TNOVuhP7qv05awogom2'

with open('instructorTool/courseslist.json') as f:
        courses = json.load(f)

@app.route("/")
@app.route("/login")
def login():
    return render_template('login.html',title ="Login",courses= courses)

@app.route("/home")
@login_required
def home():
    return render_template('home.html',title ="Home",courses= courses)

@app.route("/about")
@login_required
def about():
    return render_template('about.html')

@app.route("/cal")
@login_required
def cal():
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.getallevents(course)
    print(result['assignments'])
    myevents = json.dumps(result['events'])
    assignments = json.dumps(result['assignments'])
    return render_template('calendar.html', events = myevents, assignments = assignments, course= "course_"+course)

@app.route("/newevent", methods=['POST'])
@login_required
def newEvents():
    response = request.data
    responseObj = json.loads(response)
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.create_event(responseObj)
    return result

@app.route("/editevent", methods=['POST'])
@login_required
def editEvents():
    response = request.data
    responseObj = json.loads(response)
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.edit_event(responseObj)
    return result

@app.route("/deleteevent", methods=['POST'])
@login_required
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
@login_required
def send():
    if request.method== 'POST':
        return render_template('coursepage.html',title = "Course Page")

    doc_url = request.args.get('file-path')
    range_pref = request.args.get('range')
    if doc_url and range_pref:
        return fetch_document(doc_url, range_pref)

    return render_template('home.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html')

@app.route("/document")
@login_required
def fetch_document(doc_id, range_pref):
    doc_id = doc_id.split("/")[5]
    range_int = int(range_pref)
    print(doc_id)
    access_token = session['access_token']
    r=requests.get("https://www.googleapis.com/drive/v3/files/"+doc_id+"/export?mimeType=text/csv", headers={"Authorization":access_token})
   
    destname = 'dummy.csv'
    with open(destname, 'w') as wf:
        wf.write(r.text)
        
    count = 0
    with open(destname, 'r') as rf:
        rawtext = rf.read().splitlines()
        myreader = csv.reader(rawtext)
        res = []
        no_of_pref = range_int
        no_of_avoid = range_int
        for row in myreader:
            print("-----------------------------------------------------------------------")
            count = count + 1
            if(count % 2 != 0):
                try:
                    temp = []
                    i = 1
                    temp.append(row[i])
                    i+=1
                    temp.append(row[i])
                    i+=1
                    temp.append(row[i])
                    i+=1
                    temp.append(row[i])
                    i += 1
                    pref = []
                    for k in range(i, no_of_pref+i):
                        #print(line[k])
                        if row[k] != '' and row[k] != ' ':
                            #print(line[k])
                            pref.append(row[k])
                    temp.append(pref)
                    i += no_of_pref
                    avoid = []
                    for k in range(i, no_of_avoid+i):
                        if row[k] != '' and row[k] != ' ':
                            avoid.append(row[k])
                    temp.append(avoid)
                    i += no_of_avoid
                    temp.append(row[i])
                    i += 1
                    date_time = []
                    for idx,word in enumerate(row[i].split(',')):
                        if idx%2 == 0:
                            first = word
                        else:
                            date_time.append(first + '-' + word)

                    temp.append(date_time)
                    i += 1
                    temp.append(row[i])
                    i += 1
                    temp.append(row[i])
                    i += 1
                    temp.append(row[i])
                    res.append(temp)
                    print(temp)
                except:
                    traceback.print_exc(file=sys.stdout)

        data = pd.DataFrame(res, columns=['Full Name', 'ASURITE', 'GitHub', 'EmailID', 'Preferences', 'Avoidance', 'TimeZone', 'TimePreference', 'GithubKnowledge', 'ScrumKnowledge', 'Comments'])
        print(data)

    return data.to_json(orient='split')

@app.route("/oauthcallback")
def callback():
    code = request.args.get('code')
    client_id = Configuration.query.filter_by(key="oauth_client_id").first().value
    client_secret = Configuration.query.filter_by(key="oauth_client_secret").first().value
    redirect_uri = getConfig("aws_redirect_uri", "http://127.0.0.1:5000/oauthcallback")
    PARAMS = {'code':code, 'client_id': client_id, 
    'client_secret': client_secret, 'redirect_uri': redirect_uri,
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
    domain = email.split('@')[1]
    if domain != "asu.edu":
        return "Please login via asu.edu account"
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
    return redirect(url_for('token'))

@app.route("/google")
def sendrequest():
    client_id = Configuration.query.filter_by(key="oauth_client_id").first().value
    redirect_uri = getConfig("aws_redirect_uri", "http://127.0.0.1:5000/oauthcallback")
    url = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id="\
    + str(client_id)\
    +"&scope=https://www.googleapis.com/auth/spreadsheets+https://www.googleapis.com/auth/drive.file+https://www.googleapis.com/auth/drive+email+profile&redirect_uri="\
    + redirect_uri
    return redirect(url)

@app.route("/initconfig")
@login_required
def initdatabase():
    return render_template('initconfig.html')

def getConfig(config_name, default):
    config = Configuration.query.filter_by(key=config_name).first()
    if config:
        return config.value
    else:
        return default

@app.route("/addconfig")
@login_required
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

@app.route("/token")
@login_required
def token():
   return render_template('token.html') 

