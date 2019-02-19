from canvasapi import Canvas
import json
API_URL = "https://asu.instructure.com"
API_KEY = "7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42"
canvas = Canvas(API_URL, API_KEY)

def getallevents():
    courses = canvas.get_courses()
    user = canvas.get_user('self')
    courses_array = []
    user_array = []
    resultant_json_format = {"events":[], "assignments":[]}
    for course in courses:
        courses_array.append('course_' + str(course.id))
    user_array.append('user_' + str(user.id))
    course_events = canvas.get_calendar_events(all_events = 1, type = 'event', context_codes=courses_array)
    user_events = canvas.get_calendar_events(all_events = 1, type = 'event', context_codes=user_array)
    course_assignments = canvas.get_calendar_events(all_events = 1, type = 'assignment', context_codes=courses_array)
    for event in course_events:
        resultant_json_format["events"].append(event.__dict__['attributes'])
    for event in user_events:
        resultant_json_format["events"].append(event.__dict__['attributes'])
    for assignment in course_assignments:
        resultant_json_format["assignments"].append(assignment.__dict__['assignment'])

    with open('calendar.json', 'a') as fp:
            json.dump(resultant_json_format, fp, indent = 4)

