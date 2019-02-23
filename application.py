from flask import Flask, render_template, url_for,json, request
app = Flask(__name__)

with open('courseslist.json') as f:
    courses = json.load(f)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title ="Home",courses= courses)

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