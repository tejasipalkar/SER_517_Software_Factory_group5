from flask import Flask,render_template
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired 

 
app = Flask(__name__)
app.config['SECRET_KEY']= 'Secret'

class TokenForm(Form):
	tokenid = StringField('tokenid',validators =[InputRequired()])

@app.route('/', methods =['GET', 'POST'])
def form(): 
	form =TokenForm()
	if form.validate_on_submit():
		return 'Form Successfully submitted'
	return render_template('form.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)