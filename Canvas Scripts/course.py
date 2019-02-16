from canvasapi import Canvas
API_URL = "https://asu.instructure.com"
API_KEY = "7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42"
canvas = Canvas(API_URL, API_KEY)

courses = canvas.get_courses()
counter = 0
for vals in courses:
    if counter == 3:
        term = vals.get_enrollments()
        users = vals.get_users()
    counter = counter + 1

for vals in term:
    if vals.type == "TeacherEnrollment":
        user_id = vals.user_id

for vals in users:
   if vals.id == user_id:
        instructor_name = vals.name

print(instructor_name)
