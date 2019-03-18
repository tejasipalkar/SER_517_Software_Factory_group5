from flask import Flask, render_template, url_for,json, request
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired 

app = Flask(__name__)
app.config['SECRET_KEY']= 'Secret'

# class TokenForm(Form):
# 	tokenid = StringField('tokenid',validators =[InputRequired()])

# @app.route('/', methods =['GET', 'POST'])
# def form(): 
# 	form =TokenForm()
# 	if form.validate_on_submit():
# 		return 'Form Successfully submitted'
# 	return render_template('form.html', form=form)

with open('courseslist.json') as f:
    courses = json.load(f)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title ="Home",courses= courses)

@app.route("/newLogin")
def newLogin():
    return render_template('newLogin.html',title ="Login")


@app.route("/about")
def about():
    return render_template('about.html',title ="About")

@app.route("/login")
def login():
	return render_template('login.html', title="Login")

@app.route("/")

@app.route('/send', methods=['GET','POST'])
def send():
    if request.method== 'POST':
        return render_template('coursepage.html',title = "Course Page")

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)