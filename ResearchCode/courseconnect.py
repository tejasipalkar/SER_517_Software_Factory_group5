from canvasapi import Canvas
import json

class CourseConnect:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def getcourse(self):
        courses = self.canvas.get_courses()
        course_dict = dict()
        for course in courses:
            course_name = course.name
            enrollments = course.get_enrollments()
            for enrollment in enrollments:
                if enrollment.type == "TeacherEnrollment":
                    user_id = enrollment.user_id
            users = course.get_users()
            for user in users:
                if user.id == user_id:
                    instructor_name = user.name

            if course_name not in course_dict:
                course_dict[course_name] = instructor_name

        return course_dict

course = CourseConnect("Input_token_key")
available_course = course.getcourse()
for c in available_course:
    print(c)
