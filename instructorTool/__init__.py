from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fe36a4a2322786622f1ef490c59b8b2f'

from instructorTool import routes