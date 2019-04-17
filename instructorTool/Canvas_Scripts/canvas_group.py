from canvasapi import Canvas

class Canvas_Group:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def create_groups(self, dictvals, courseid):
        course = self.canvas.get_course(courseid)
        users = course.get_users()
        user_dict = {}
        exceptval = ""
        for user in users:
            if 'email' in user.__dict__:
                user_dict[user.email] = user.id
        try:
            group_category = course.create_group_category("Project Group")
        except:
            exceptval = 'Group Set Already Exists'
            return exceptval

        for key, value in dictvals.items():
            group_name = str(key)
            try:
                group = group_category.create_group(name = group_name)
            except:
                exceptval = 'Group Already Exists'
                return exceptval
            members = []
            for vals in value:
                if vals in user_dict:
                    members.append(user_dict[vals])
            try:
                group = group.edit(members = members)
            except:
                exceptval = 'These Members are Already Present In The Group: ' + group_name
                return exceptval
        exceptval = 'Groups Pushed to Canvas'
        return exceptval


