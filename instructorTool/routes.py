from flask import render_template, url_for, json, flash, redirect, request
from instructorTool import app
from instructorTool.forms import LoginForm
from instructorTool.Canvas_Scripts.canvas_calendar import Canvas_Calendar
import json

course = 'course_15760'
canvas_token = "7236~p8bdXeGzlCNwcTIiFvdetkcTmS1MHMKyinjnPFQLVOAunOvE8kyzue4fUock3u4V"

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
    print(result['events'])
    myevents = json.dumps(result['events'])
    return render_template('calendar.html', events = myevents, course= course)

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
    return redirect(url_for('home'))

@app.route("/account")
#@login_required
def account():
    return render_template('account.html')