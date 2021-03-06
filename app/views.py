from flask import Flask, render_template, request, flash, session, redirect, url_for, request, g
from app import app, db, models
from config import MAX_SEARCH_RESULTS, CB_API_KEY
from forms import LoginForm, SignupForm, NewContact, EditContact, SearchForm
from models import db, User, Contact
from datetime import datetime
import pycrunchbase

cb = pycrunchbase.CrunchBase(CB_API_KEY)

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
    searchform = SearchForm()
    return render_template('list.html', user=user, contacts=contacts, searchform=searchform)


@app.route('/list_item/<contactid>')
def list_item(contactid):
  searchform = SearchForm()
  contact = Contact.query.filter_by(id = contactid).first()
  columns = ['company', 'email', 'mobile', 'work', 'home', 'created']
  attributes = []
  labels = []
  for column in columns:
    info = getattr(contact, column, [''])
    if (str(info) != ''):
        attributes.append(info)
        labels.append(column)
  co_name = str(getattr(contact, 'company', ['']))
  if (co_name != ''):
    return render_template('list_item_plusco.html', contact=contact, searchform=searchform, attributes=attributes, labels=labels, company=cb.organization(co_name))
  else:
    return render_template('list_item.html', contact=contact, searchform=searchform, attributes=attributes, labels=labels)


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
  searchform = SearchForm()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('add.html', form=form, searchform=searchform)
    else:
      time = datetime.now()
      newcontact = Contact(form.firstname.data, form.lastname.data, form.email.data, form.mobile.data, form.work.data, form.home.data, form.company.data, user.uid, time)
      db.session.add(newcontact)
      db.session.commit()
      contact = Contact.query.filter_by(created = time).first()
      return redirect(url_for('list_item', contactid=contact.id))
          
  elif request.method == 'GET':
    return render_template('add.html', form=form, searchform=searchform)


@app.route('/edit/<contactid>', methods=['GET', 'POST'])
def edit(contactid):

  if 'email' not in session:
    return redirect(url_for('login'))

  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('login'))

  contact = Contact.query.filter_by(id = contactid).first()
  form = EditContact()
  searchform = SearchForm()
    
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('edit.html', form=form, searchform=searchform)
    else:
      contact.firstname = form.firstname.data
      contact.lastname = form.lastname.data
      contact.email = form.email.data      
      contact.mobile = form.mobile.data
      contact.work = form.work.data
      contact.home = form.home.data
      contact.company = form.company.data

      db.session.commit()
      flash('User Updated')
      return redirect(url_for('list_item', contactid=contact.id))
          
  elif request.method == 'GET':
    form.firstname.data = contact.firstname
    form.lastname.data = contact.lastname
    form.email.data = contact.email
    form.mobile.data = contact.mobile
    form.work.data = contact.work
    form.home.data = contact.home
    form.company.data = contact.company
    return render_template('edit.html', form=form, searchform=searchform)


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
      searchform = SearchForm()
      return render_template('search_results.html',
                           user=user,
                           query=query,
                           results=results,
                           searchform=searchform)