# Instructor-tool-for-team-based-courses

Dependencies:
1. flask-sqlalchemy
2. flask-login

Setup AlchemySQL DB
1. Under porject folder start python
2. run: from instructorTool import db
3. run: from instructorTool.models import User
4. run: db.create_all()
5. The db and Users table is successfully created.
6. Now you can add some dummy data, using the following commands:
    a. user_1 = User(username='Karan',email='kbhangal@asu.edu',password='1234')
    b. db.session.add(user_1)
    c. db.session.commit()
