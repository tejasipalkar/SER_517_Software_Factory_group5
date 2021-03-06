from canvasapi import Canvas
from taiga import TaigaAPI
import requests

class STG_Group:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def get_groupsdata(self, course_id):
        group_data = {}
        course = self.canvas.get_course(course_id)
        group_categories = course.get_group_categories()
        for categories in group_categories:
            if categories.name == "Project Group":
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
        res = requests.put('https://slack.com/api/users.list?token='+token+'&pretty=1')
        data = res.json()
        if "error" in data:
            return data["error"]
        else:
            members = data["members"]
            nameToID = {}
            for i in range(0, len(members)):
                nameToID[members[i]['name']] = members[i]['id']

            group_append = ["-inst", "-gen"]

            for key in group_data:
                name = key
                groupMembers = group_data[key]
                channelIDs = []

                if len(group_append) == 0:
                    res = requests.put('https://slack.com/api/groups.create?token='+token+'&name='+name+'&pretty=1')
                    data = res.json()
                    channelIDs.append(data["group"]['id'])
                else:
                    for append in group_append:
                        name1 = name + append
                        res = requests.put('https://slack.com/api/groups.create?token='+token+'&name='+name1+'&pretty=1')
                        data = res.json()
                        channelIDs.append(data["group"]['id'])

                for i in range(0, len(groupMembers)):
                    userID = nameToID[groupMembers[i]]
                    for channelID in channelIDs:
                        res = requests.put('https://slack.com/api/groups.invite?token='+token+'&channel='+channelID+'&user='+userID+'&pretty=1')

    def create_taiga_channels(self, username, password, desc, course_id):
        api = TaigaAPI()
        try:
            api.auth(
                username=username,
                password=password
            )
        except:
            return 'invalid auth'
        group_data = self.get_groupsdata(course_id)
        for key in group_data:
            new_project = api.projects.create(key, desc)
            new_project.is_private="false"
            new_project.update()

            for member in group_data[key]:
                email = member+'@asu.edu'
                new_project.add_membership(role = new_project.roles[0].id, username = email, email = email)
