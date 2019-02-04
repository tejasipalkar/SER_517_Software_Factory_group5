from flask import Flask, render_template, url_for,json
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

if __name__ == '__main__':
    app.run(debug=True)