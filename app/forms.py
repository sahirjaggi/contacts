from flask.ext.wtf import Form, validators
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from models import db, User

class LoginForm(Form):
  email = StringField('email', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])
  remember_me = BooleanField('remember_me', default=False)
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False

class SignupForm(Form):
	firstname = StringField('firstname', validators=[DataRequired()])
	lastname = StringField('lastname', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
 
	def __init__(self, *args, **kwargs):
	    Form.__init__(self, *args, **kwargs)
	 
	def validate(self):
	    if not Form.validate(self):
	      return False
	     
	    user = User.query.filter_by(email = self.email.data.lower()).first()
	    if user:
	      self.email.errors.append("That email is already taken")
	      return False
	    else:
	      return True

class NewContact(Form):
	firstname = StringField('firstname', validators=[DataRequired()])
	lastname = StringField('lastname', default=None)
	email = StringField('email', default=None)
	mobile = StringField('mobile', default=None)
	work = StringField('work', default=None)
	home = StringField('home', default=None)
 
	def __init__(self, *args, **kwargs):
	    Form.__init__(self, *args, **kwargs)
	 
	def validate(self):
	    if not Form.validate(self):
	      return False
	    else:
	      return True

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])