from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

import sys
if sys.version_info >= (3, 0):
	enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))
	contacts = db.relationship('Contact', backref='owner', lazy='dynamic', primaryjoin="Contact.user_id==User.uid")
   
	def __init__(self, firstname, lastname, email, password):
	  	self.firstname = firstname.title()
	  	self.lastname = lastname.title()
	  	self.email = email.lower()
	  	self.set_password(password)
	     
	def set_password(self, password):
	    self.pwdhash = generate_password_hash(password)
	   
	def check_password(self, password):
	    return check_password_hash(self.pwdhash, password)

class Contact(db.Model):
	__tablename__ = 'contacts'
	__searchable__ = ['firstname', 'lastname']

	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120))
	mobile = db.Column(db.String(20))
	work = db.Column(db.String(20))
	home = db.Column(db.String(20))
	user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
	created = db.Column(db.DateTime)

	def __init__(self, firstname, lastname, email, mobile, work, home, user_id, created):
	  	self.firstname = firstname.title()
	  	self.lastname = lastname.title()
	  	self.email = email.title()
	  	self.mobile = mobile.title()
	  	self.work = work.title()
	  	self.home = home.title()
	  	self.user_id = user_id
	  	self.created = created
	
	def __repr__(self):
		return '<Contact %r>' % (self.firstname)

if enable_search:
    whooshalchemy.whoosh_index(app, Contact)