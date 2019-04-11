from instructorTool.Canvas_Scripts.stg_grouping import Github
from instructorTool.models import User, Configuration
from instructorTool import app
from flask import render_template, url_for, json, flash, redirect, request


@app.route("/testcase/create_githubrepo")
def test_repo_creation():
	user = Configuration.query.filter_by(key='repo.owner').first().value
	token = Configuration.query.filter_by(key='repo.personal.access.token').first().value
	obj = Github(user, token)
	if(obj.create_github_repo("test_repo") == 'Status: 201 Created'):
		return "Github repo creation successful"
	else:
		return "Github repo creation failed"


