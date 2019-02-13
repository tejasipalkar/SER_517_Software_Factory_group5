from flask import render_template, url_for, json, flash, redirect, request
from instructorTool import app
from instructorTool.forms import LoginForm
from instructorTool.models import User
from flask_login import login_user, current_user, logout_user, login_required

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

@app.route('/send', methods=['GET','POST'])
def send():
    if request.method== 'POST':
        return render_template('coursepage.html',title = "Course Page")

    return render_template('home.html')

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