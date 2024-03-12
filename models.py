from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import validates, relationship, backref
from flask_security import UserMixin, RoleMixin, AsaList

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    # username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    # last_login_at = db.Column(db.DateTime())
    # current_login_at = db.Column(db.DateTime())
    # last_login_ip = db.Column(db.String(100))
    # current_login_ip = db.Column(db.String(100))
    # login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    # confirmed_at = db.Column(db.DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

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