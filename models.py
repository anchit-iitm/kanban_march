from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    userid = db.Column(db.Integer, autoincrement=True, primary_key=True) #user
    username = db.Column(db.String, unique=True, nullable=False)#user's login id		
    passkey = db.Column(db.String, nullable=False)				#user's password

class list(db.Model):
	list_id = db.Column(db.Integer, autoincrement=True, primary_key=True) #list
	list_name = db.Column(db.String, nullable=False)			#list title
	list_desc = db.Column(db.String, nullable=False)			#list description
	user_id = db.Column(db.String, nullable=True)				#list of which user
	list_c_date = db.Column(db.String)							#list made on
	list_u_date = db.Column(db.String)							#list last updated on

class task(db.Model):
	task_id = db.Column(db.Integer, autoincrement=True, primary_key=True) #task
	list_id = db.Column(db.Integer, nullable=False)				#task of which list
	task_title = db.Column(db.String, nullable=False)			#task title
	task_content = db.Column(db.String, nullable=False)			#task description
	task_deadline = db.Column(db.String)						#task deadline
	task_complete = db.Column(db.Integer)						#task status
	task_c_date = db.Column(db.String)							#creating date
	task_u_date = db.Column(db.String)							#updating date
	task_d_date = db.Column(db.String)							#completing date