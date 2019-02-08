from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fe36a4a2322786622f1ef490c59b8b2f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instructor.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from instructorTool import routes