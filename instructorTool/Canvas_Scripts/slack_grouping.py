from canvasapi import Canvas
import requests

class slack_group:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def get_groupsdata(self, course_id):
        group_data = {}
        course = self.canvas.get_course(course_id)
        group_categories = course.get_group_categories()
        for categories in group_categories:
            if categories.name == "Project":
                group_category = categories
        groups = group_category.get_groups()
        for group in groups:
            users = group.get_users()
            members = []
            for user in users:
                members.append(user.login_id)
            group_data[group.name] = members
        return group_data

    def create_slack_groups(self, token, course_id):
        group_data = self.get_groupsdata(course_id)
        # Not accepting the access token and not authorizing.
        res = requests.get('https://slack.com/api/auth.test?token='+token)
        data = res.json()
        print(data)

