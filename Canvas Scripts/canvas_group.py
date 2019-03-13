from canvasapi import Canvas
import csv

class Canvas_Group:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def create_groups(self, csv_loc, course):
        course_id = 0
        result = {}
        courses = self.canvas.get_courses()
        for vals in courses:
            if vals.name.lower() == course.lower():
                course_id = vals.id

        course = self.canvas.get_course(course_id)
        users = course.get_users()
        user_dict = {}
        for user in users:
            if 'email' in user.__dict__:
                user_dict[user.email] = user.id

        with open(csv_loc, mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                array = rows[1].split(',')
                for val in range(0, len(array)):
                    array[val] = array[val].strip(' ')
                    array[val] = array[val].strip('\'')
                result[rows[0]] = array

        group_category = course.create_group_category("Project Group")

        for key, value in result.items():
            group_name = str(key)
            group = group_category.create_group(name = group_name)
            members = []
            for vals in value:
                if vals in user_dict:
                    members.append(user_dict[vals])
            group = group.edit(members = members)

# group = Canvas_Group(API Key)
group = Canvas_Group("7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42")

# group.create_groups(CSV Location, Name Of The Course)
group.create_groups("groups.csv","SER515-Group5-TestShell")
