from flask import Flask, render_template, url_for
app = Flask(__name__)

courses =[{
    'name':'SER 517',
    'Instructor' :'Heinrich Reimer'
    },
    {
        'name' : 'SER 515',
        'Instructor' :'Alexandra Mehlhase'
    
    },
    {
        'name' : 'SER 422',
        'Instructor' :'Kevin Gary'
    
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title ="Home",courses= courses)



@app.route("/about")
def about():
    return render_template('about.html',title ="About")

if __name__ == '__main__':
    app.run(debug=True)