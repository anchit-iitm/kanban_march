from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, AsaList
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship, backref

# commment to check how the checksum value changes

db = SQLAlchemy()

class List(db.Model): # list
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    c_date = db.Column(db.String) #create date
    u_date = db.Column(db.String) #update date

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255))
    deadline = db.Column(db.String)
    complete = db.Column(db.Integer) # contains the list id of the list which it was marked as completed, if it was list.id=1, then the value would be 1
    c_date = db.Column(db.String) # date of creation
    u_date = db.Column(db.String) # date of update if there is any
    d_date = db.Column(db.String) # date of completion / done date


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
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))