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
        res = requests.put('https://slack.com/api/users.list?token='+token+'&pretty=1')
        data = res.json()
        if "error" in data:
            return data["error"]
        else:
            members = data["members"]
            nameToID = {}
            for i in range(0, len(members)):
                nameToID[members[i]['name']] = members[i]['id']

            group_append = ["_instructor", "_general"]

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
                        res = requests.put('https://slack.com/api/groups.create?token='+token+'&name='+name+append+'&pretty=1')
                        data = res.json()
                        channelIDs.append(data["group"]['id'])

                for i in range(0, len(groupMembers)):
                    userID = nameToID[groupMembers[i]]
                    for channelID in channelIDs:
                        res = requests.put('https://slack.com/api/groups.invite?token='+token+'&channel='+channelID+'&user='+userID+'&pretty=1')

    def create_taiga_channels(self, username, password, desc, course_id):
        api = TaigaAPI()
        api.auth(
            username=username,
            password=password
        )
        group_data = self.get_groupsdata(course_id)
        for key in group_data:
            new_project = api.projects.create(key, desc)
            new_project.is_private="false"
            new_project.update()

            for member in group_data[key]:
                email = member+'@asu.edu'
                new_project.add_membership(role = new_project.roles[0].id, username = email, email = email)


    def create_github_repo(self, repo_name):
        description = 'Welcome to ' + repo_name
        payload = {'name': repo_name, 'description': description, 'auto_init': 'true', "private": 'true'}
        user = Configuration.query.filter_by(key='repo.owner').first().value
        token = Configuration.query.filter_by(key='repo.personal.access.token').first().value
        requests.post('https://api.github.com/' + 'user/repos', auth=(owner,token), data=json.dumps(payload))


    def add_collaborator(self, repo_name, username):
        owner = Configuration.query.filter_by(key='repo.owner').first().value
        token = Configuration.query.filter_by(key='repo.personal.access.token').first().value
        requests.put('https://api.github.com/' + 'repos/' + owner +'/' + repo_name + '/collaborators/' + username, auth=(owner,token))


