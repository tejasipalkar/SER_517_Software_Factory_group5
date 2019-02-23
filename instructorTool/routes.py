from flask import render_template, url_for, json, flash, redirect, request
from instructorTool import app
from instructorTool.forms import LoginForm

#if logged-in only then take user to home page and show list of courses
# else redirect user to login page and show alert that they need to log in first
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
    return render_template('calendar.html')

@app.route('/send', methods=['GET','POST'])
def send():
    if request.method== 'POST':
        return render_template('coursepage.html',title = "Course Page")

    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    return redirect(url_for('home'))

@app.route("/account")
#@login_required
def account():
    return render_template('account.html')