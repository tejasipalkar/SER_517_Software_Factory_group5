from flask import render_template, url_for, json, flash, redirect, request
from instructorTool import app
from instructorTool.forms import LoginForm
from instructorTool.Canvas_Scripts.canvas_calendar import Canvas_Calendar
import json

course = 'course_15760'
canvas_token = "7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42"

with open('instructorTool/courseslist.json') as f:
        courses = json.load(f)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title ="Home",courses= courses)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/cal")
def cal():
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.getallevents(course)
    print(result['events'])
    myevents = json.dumps(result['events'])
    #'[{             "id": 59221,             "title": "sfjkdansbj",             "start_at": "2019-03-19T23:59:00-06:00",             "unlock_at": null,             "end_at": "2019-03-20T23:59:00-06:00",             "points_possible": 0.0,             "grading_type": "pass_fail",             "assignment_group_id": 17727,             "grading_standard_id": null,             "created_at": "2018-08-15T03:05:55Z",             "updated_at": "2018-12-20T04:52:04Z",             "peer_reviews": false,             "automatic_peer_reviews": false,             "position": 1,             "grade_group_students_individually": false,             "anonymous_peer_reviews": false,             "group_category_id": null,             "post_to_sis": false,             "moderated_grading": false,             "omit_from_final_grade": false,             "intra_group_peer_reviews": false,             "anonymous_instructor_annotations": false,             "anonymous_grading": false,             "graders_anonymous_to_graders": false,             "grader_count": null,             "grader_comments_visible_to_graders": true,             "final_grader_id": null,             "grader_names_visible_to_final_grader": true,             "allowed_attempts": -1,             "lock_info": {                 "lock_at": "2018-08-21T06:59:00Z",                 "can_view": true,                 "asset_string": "assignment_59221"             },             "secure_params": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsdGlfYXNzaWdubWVudF9pZCI6IjEzOTc3YzgwLWZlYTMtNDU2ZS1hMDBmLTFkNDEzMjYyZDczNSJ9.R_UF0CZtaJp9vRi4MgfkCinPxpFm1ybxQIQfe2KhpcY",             "course_id": 3682,             "name": "Week 1 Response Doc",             "submission_types": [                 "online_upload"             ],             "has_submitted_submissions": true,             "due_date_required": false,             "max_name_length": 255,             "in_closed_grading_period": false,             "user_submitted": true,             "is_quiz_assignment": false,             "can_duplicate": true,             "original_course_id": null,             "original_assignment_id": null,             "original_assignment_name": null,             "workflow_state": "published",             "muted": false,             "html_url": "https://asu.instructure.com/courses/3682/assignments/59221",             "allowed_extensions": [                 "pdf",                 "pdf"             ],             "published": true,             "only_visible_to_overrides": false,             "locked_for_user": true,             "lock_explanation": "This assignment was locked Aug 20, 2018 at 11:59pm.",             "submissions_download_url": "https://asu.instructure.com/courses/3682/assignments/59221/submissions?zip=1",             "anonymize_students": false         }]'
    return render_template('calendar.html', events = myevents, course= course)

@app.route("/newevent", methods=['POST'])
def newEvents():
    response = request.data
    responseObj = json.loads(response)
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.create_event(responseObj)
    return result

@app.route("/editevent", methods=['POST'])
def editEvents():
    response = request.data
    responseObj = json.loads(response)
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.edit_event(responseObj)
    return result

@app.route("/deleteevent", methods=['POST'])
def deleteEvents():
    response = request.data
    responseObj = json.loads(response)
    canvas = Canvas_Calendar(canvas_token)
    result = canvas.delete_event(responseObj)
    return result

@app.route('/send', methods=['GET','POST'])
def send():
    if request.method== 'POST':
        return render_template('coursepage.html',title = "Course Page")

    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    return redirect(url_for('home'))

@app.route("/account")
#@login_required
def account():
    return render_template('account.html')