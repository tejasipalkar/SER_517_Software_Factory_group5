from canvasapi import Canvas

class Course:
    def __init__(self):
        self.API_URL = "https://asu.instructure.com"
        self.API_KEY = "7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42"
        self.canvas = Canvas(self.API_URL, self.API_KEY)

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


