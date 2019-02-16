from canvasapi import Canvas
API_URL = "https://asu.instructure.com"
API_KEY = "7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42"
canvas = Canvas(API_URL, API_KEY)

def getcourse():
    courses = canvas.get_courses()
    course_dict = dict()
    for vals in courses:
        course_name = vals.name
        enrollments = vals.get_enrollments()
        for items in enrollments:
            if items.type == "TeacherEnrollment":
                user_id = items.user_id
        users = vals.get_users()
        for items in users:
            if items.id == user_id:
                instructor_name = items.name

        if course_name not in course_dict:
            course_dict[course_name] = instructor_name

    return course_dict


