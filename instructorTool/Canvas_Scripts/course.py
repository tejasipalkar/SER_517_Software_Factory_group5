from canvasapi import Canvas
import json

class Course:
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

    def getcoursejson(self):
        course_dict = self.getcourse()
        course_json_format = {"type":"course",
                        "children":[{"name'":key,"instructor":value} for key, value in course_dict.items()]}
        with open('course.json', 'w') as fp:
            json.dump(course_json_format, fp, indent = 4)


