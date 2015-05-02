from flask import Flask, render_template, request, flash, session, redirect, url_for, request, g
from app import app, db, models
from config import MAX_SEARCH_RESULTS
from forms import LoginForm, SignupForm, NewContact, SearchForm
from models import db, User, Contact
from datetime import datetime

@app.route('/')

@app.route('/index')
def index():

  if 'email' in session:
    return redirect(url_for('list'))
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

  if 'email' in session:
  	return redirect(url_for('list'))

  form = SignupForm()
   
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

  if 'email' in session:
  	return redirect(url_for('list'))

  form = LoginForm()
   
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
    return redirect(url_for('login'))
     
  session.pop('email', None)
  return redirect(url_for('login'))


@app.route('/list')
def list():
 
  if 'email' not in session:
    return redirect(url_for('login'))
 
  user = User.query.filter_by(email = session['email']).first()
  contacts = user.contacts.order_by(Contact.firstname).all()
 
  if user is None:
    return redirect(url_for('login'))
  else:
    form = SearchForm()
    return render_template('list.html', user=user, contacts=contacts, form=form)


@app.route('/list_item/<contactid>')
def list_item(contactid):
  contact = Contact.query.filter_by(id = contactid).first()
  return render_template('list_item.html', contact=contact)


@app.route('/delete/<contactid>')
def delete(contactid):
  contact = Contact.query.filter_by(id = contactid).first()
  db.session.delete(contact)
  db.session.commit()
  return redirect(url_for('list'))


@app.route('/add', methods=['GET', 'POST'])
def add():

  if 'email' not in session:
  	return redirect(url_for('login'))

  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('login'))
  form = NewContact()
  
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


@app.route('/edit/<contactid>', methods=['GET', 'POST'])
def edit(contactid):
  form = EditContact()

  if 'email' not in session:
    return redirect(url_for('login'))

  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('login'))

  contact = Contact.query.filter_by(id = contactid).first()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('add.html', form=form)
    else:
      contact.firstname = form.firstname.data
      contact.lastname = form.lastname.data
      contact.email = form.email.data      
      contact.mobile = form.mobile.data
      db.session.commit()
      flash('User Updated')
      return redirect(url_for('list_item', contactid=contact.id))
          
  elif request.method == 'GET':
    form.firstname.data = contact.firstname
    form.lastname.data = contact.lastname
    form.email.data = contact.email
    form.mobile.data = contact.mobile
    return render_template('add.html', form=form)


@app.route('/search', methods=['POST'])
def search():
    if 'email' not in session:
      return redirect(url_for('login'))
 
    user = User.query.filter_by(email = session['email']).first()
 
    if user is None:
      return redirect(url_for('login'))
    else:
      return redirect(url_for('search_results', query=request.form.get('search')))


@app.route('/search_results/<query>')
def search_results(query):
 
    if 'email' not in session:
      return redirect(url_for('login'))
 
    user = User.query.filter_by(email = session['email']).first()
 
    if user is None:
      return redirect(url_for('login'))
    else:
      term = query+'*'
      results = Contact.query.whoosh_search(term, MAX_SEARCH_RESULTS).all()
      form = SearchForm()
      return render_template('search_results.html',
                           user=user,
                           query=query,
                           results=results,
                           form=form)