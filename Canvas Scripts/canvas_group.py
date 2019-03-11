from canvasapi import Canvas
API_URL = "https://asu.instructure.com"
api_key = "7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42"
canvas = Canvas(API_URL, api_key)

course = canvas.get_course(15760)
group_category = course.create_group_category("Project Group")
group_name = 'test'
group = group_category.create_group(name = group_name)
user = [107421, 30029]
group = group.edit(members = user)
