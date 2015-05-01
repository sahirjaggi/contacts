from flask import Flask, render_template, request, flash, session, redirect, url_for, request, g
from app import app, db, models
from config import MAX_SEARCH_RESULTS
from forms import LoginForm, SignupForm, NewContact, SearchForm
from models import db, User, Contact
from datetime import datetime

@app.route('/')

@app.before_request
def before_request():
    if 'email' not in session:
        return redirect(url_for('login'))

    g.user = User.query.filter_by(email = session['email']).first()
 
    if g.user is None:
        return redirect(url_for('login'))
    else:
        #g.user.last_seen = datetime.utcnow()
        #db.session.add(g.user)
        #db.session.commit()
        g.search_form = SearchForm()
        return

@app.route('/index')
def index():

    if 'email' not in session:
      return redirect(url_for('login'))
    
    user = User.query.filter_by(email = session['email']).first()
    userid = user.uid

    if user is None:
      return redirect(url_for('login'))

    contacts = Contact.query.filter_by(user_id=userid).order_by(Contact.firstname).all()

    return render_template("index.html",
                           title='Home',
                           user=user,
                           contacts=contacts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
  	return redirect(url_for('list'))
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('list'))

  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if 'email' in session:
  	return redirect(url_for('list'))
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('login.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('list'))
                 
  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
 
  if 'email' not in session:
    return redirect(url_for('logout'))
     
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route('/list')
def list():
  form = SearchForm()
 
  if 'email' not in session:
    return redirect(url_for('login'))
 
  user = User.query.filter_by(email = session['email']).first()
  contacts = user.contacts.all()
 
  if user is None:
    return redirect(url_for('login'))
  else:
    return render_template('list.html', user=user, contacts=contacts, form=form)

##@app.route('/list_item/<contactid>')
##def list_item(contactid):
  ##  return render_template('list_item.html', contact=contactid)

@app.route('/add', methods=['GET', 'POST'])
def add():
  form = NewContact()

  if 'email' not in session:
  	return redirect(url_for('login'))

  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('login'))
  
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('add.html', form=form)
    else:
      newcontact = Contact(form.firstname.data, form.lastname.data, form.email.data, form.mobile.data, form.work.data, form.home.data, user.uid, datetime.now())
      db.session.add(newcontact)
      db.session.commit()

      return redirect(url_for('list'))
          
  elif request.method == 'GET':
    return render_template('add.html', form=form)

@app.route('/search', methods=['POST'])
def search():
    if 'email' not in session:
      return redirect(url_for('login'))
 
    user = User.query.filter_by(email = session['email']).first()
 
    if user is None:
      return redirect(url_for('login'))
    else:
      if not g.search_form.validate_on_submit():
        return redirect(url_for('list'))
      return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
def search_results(query):
    term = '*'+query+'*'
    results = Contact.query.whoosh_search(term, MAX_SEARCH_RESULTS).all()
    form = g.search_form
 
    if 'email' not in session:
      return redirect(url_for('login'))
 
    user = User.query.filter_by(email = session['email']).first()
 
    if user is None:
      return redirect(url_for('login'))
    else:
      return render_template('search_results.html',
                           user=user,
                           query=query,
                           results=results,
                           form=form)