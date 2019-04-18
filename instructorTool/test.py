from instructorTool.Canvas_Scripts.github import Github
from instructorTool.models import User, Configuration
from instructorTool import app
from flask import render_template, url_for, json, flash, redirect, request
import json
import sys, os



@app.route("/run_test")
def run_test():
    return render_template('testcase.html')


@app.route("/testcase/create_githubrepo")
def create_githubrepo():
	user = Configuration.query.filter_by(key='repo.owner').first().value
	token = Configuration.query.filter_by(key='repo.personal.access.token').first().value
	obj = Github(user, token)
	response = obj.create_github_repo("test_repo")
	result = response.status_code
	if(result == 201):
		return "Github repo creation successful"
	else:
		return "Github repo creation failed :: " + str(response.json())


@app.route("/testcase/add_collaborator")
def add_collaborator():
	user = Configuration.query.filter_by(key='repo.owner').first().value
	token = Configuration.query.filter_by(key='repo.personal.access.token').first().value
	obj = Github(user, token)
	response = obj.add_collaborator("test_repo", "svganesh93")
	result = response.status_code
	if(result == 201):
		return "Github Added svganesh93 as a Collaborator successfully"
	else:
		return "Github Add Collaborator failed :: " + str(response.json())


@app.route("/testcase/unix")
def test_unix():
	owner = Configuration.query.filter_by(key='repo.owner').first().value
	token = Configuration.query.filter_by(key='repo.personal.access.token').first().value
	repo_name = Configuration.query.filter_by(key='repo.name').first().value
	username = Configuration.query.filter_by(key='repo.owner.username').first().value
	password = Configuration.query.filter_by(key='repo.owner.password').first().value
	os.system("sh /home/ec2-user/SER_517_Software_Factory_group5-master/instructorTool/test_unix.sh {0} {1} {2} {3} {4}".format(username, password, owner, name, token))
	return "success"