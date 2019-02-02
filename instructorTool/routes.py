from flask import render_template, url_for, flash, redirect
from instructorTool import app
from instructorTool.forms import LoginForm

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'kbhangal@asu.edu' and form.username.data == 'kbhangal':   #TODO: use DB
            flash(format('Login Successful. Welcome!'), 'success')
            return redirect(url_for('home'))
        else:
            flash(format('Login Unsuccessful. Please check username and password!'), 'danger')
    return render_template('login.html', title='Login', form=form)
