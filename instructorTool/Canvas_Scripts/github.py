import requests
import json

class Github:

    def __init__(self, repo_owner, api_token):
        self.repo_owner = repo_owner
        self.api_token = api_token

    def create_github_repo(self, repo_name):
        description = 'Welcome to ' + repo_name
        payload = {'name': repo_name, 'description': description, 'auto_init': 'true', "private": 'true'}
        print(self.repo_owner)
        print(self.api_token)
        return requests.post('https://api.github.com/' + 'user/repos', auth=(self.repo_owner,self.api_token), data=json.dumps(payload))
        
    def add_collaborator(self, repo_name, username):
        return requests.put('https://api.github.com/' + 'repos/' + self.repo_owner +'/' + repo_name + '/collaborators/' + username, auth=(self.repo_owner,self.api_token))

