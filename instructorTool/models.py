from instructorTool import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return "User('{}',{})".format({self.username},{self.email})