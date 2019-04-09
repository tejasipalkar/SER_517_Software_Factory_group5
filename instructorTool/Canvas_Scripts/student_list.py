from canvasapi import Canvas

class Student_List:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def get_student_list(self, course_id):
        course = self.canvas.get_course(course_id)
        users = course.get_users()
        list_users = []
        enrollments = course.get_enrollments()
        students = []
        for enroll in enrollments:
            if enroll.type == 'StudentEnrollment':
                students.append(enroll.user_id)
        for user in users:
            if 'email' in user.__dict__:
                if user.id in students:
                    list_users.append(user.email.replace('@asu.edu', ''))
        return list_users
