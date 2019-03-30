from canvasapi import Canvas
import json

class Course:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def getcourse(self):
        courses = self.canvas.get_courses()
        course_array = []
        for course in courses:
            course_name = course.name
            course_array.append(course_name)
        return course_array




