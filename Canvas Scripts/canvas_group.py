from canvasapi import Canvas
API_URL = "https://asu.instructure.com"
api_key = "7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42"
canvas = Canvas(API_URL, api_key)

course = canvas.get_course(15760)
users = course.get_users()
user_dict = {}
for user in users:
    if 'email' in user.__dict__:
        user_dict[user.email] = user.id

result = {1: ['ygoel@asu.edu', 'tpalkar@asu.edu'], 2: ['sparlapa@asu.edu', 'zsiddiq2@asu.edu', 'gsubra11@asu.edu']}

group_category = course.create_group_category("Project Group")

for key, value in result.items():
    group_name = str(key)
    group = group_category.create_group(name = group_name)
    members = []
    for vals in value:
        if vals in user_dict:
            members.append(user_dict[vals])
    group = group.edit(members = members)
