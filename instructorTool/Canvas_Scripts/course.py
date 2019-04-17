from canvasapi import Canvas
import json

class Course:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def getcourse(self):
        courses = self.canvas.get_courses()
        course_json = {}
        for course in courses:
            course_json[course.name] = course.id
        return course_json


