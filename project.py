from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from databaseSetup import Base, Cuisine, Dish, User

#create anti forgery state token
from flask import session as login_session
import random
import string

# import for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Connect to Database and create database session
engine = create_engine('sqlite:///cuisinewithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a state token to provent requests forgery.
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    
    #check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

#Disconnect - revoke a current user's token and reset their login-session
@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke curren token
    accessToken = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % accessToken
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        #response = make_response(json.dumps('Successfully disconnected.'), 200)
        #response.headers['Content-Type'] = 'application/json'
        flash("You are now logged out seccessfully! ")
        return redirect(url_for('showCuisines'))
    
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON APIs to view one cuisine Information
@app.route('/cuisine/<int:cuisine_id>/dish/JSON')
def cuisineDishJSON(cuisine_id):
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    dishes = session.query(Dish).filter_by(
        cuisine_id=cuisine_id).all()
    return jsonify(Dishes=[i.serialize for i in dishes])

# JSON APIs to one dish Information
@app.route('/cuisine/<int:cuisine_id>/dish/<int:dish_id>/JSON')
def dishJSON(cuisine_id, dish_id):
    dish = session.query(Dish).filter_by(id=dish_id).one()
    return jsonify(Dish=dish.serialize)

# JSON APIs to view all cuisines Information
@app.route('/cuisine/JSON')
def cuisineJSON():
    cuisines = session.query(Cuisine).all()
    return jsonify(cuisines=[c.serialize for c in cuisines])

# Show all cuisine
@app.route('/')
@app.route('/cuisine/')
def showCuisines():
    cuisines = session.query(Cuisine).order_by(asc(Cuisine.name))
    if 'username' not in login_session:
        return render_template('publiccuisines.html', cuisines=cuisines)
    else:
        return render_template('cuisines.html', cuisines=cuisines)

# Create a new cuisine
@app.route('/cuisine/new/', methods=['GET', 'POST'])
def newCuisine():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCuisine = Cuisine(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCuisine)
        flash('New Cuisine %s Successfully Created' % newCuisine.name)
        session.commit()
        return redirect(url_for('showCuisines'))
    else:
        return render_template('newCuisine.html')

# Edit a cuisine
@app.route('/cuisine/<int:cuisine_id>/edit/', methods=['GET', 'POST'])
def editCuisine(cuisine_id):
    editedCuisine = session.query(
        Cuisine).filter_by(id=cuisine_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCuisine.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this cuisine. Please create your own cuisine in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedCuisine.name = request.form['name']
            flash('Cuisine Successfully Edited %s' % editedCuisine.name)
            return redirect(url_for('showCuisines'))
    else:
        return render_template('editCuisine.html', cuisine=editedCuisine)


# Delete a cuisine
@app.route('/cuisine/<int:cuisine_id>/delete/', methods=['GET', 'POST'])
def deleteCuisine(cuisine_id):
    cuisineToDelete = session.query(
        Cuisine).filter_by(id=cuisine_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if cuisineToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this cuisine. Please create your own cuisine in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(cuisineToDelete)
        flash('%s Successfully Deleted' % cuisineToDelete.name)
        session.commit()
        return redirect(url_for('showCuisines', cuisine_id=cuisine_id))
    else:
        return render_template('deleteCuisine.html', cuisine=cuisineToDelete)

# Show the dishes of a cuisine
@app.route('/cuisine/<int:cuisine_id>/')
@app.route('/cuisine/<int:cuisine_id>/dish/')
def showDish(cuisine_id):
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    creator = getUserInfo(cuisine.user_id)
    dishes = session.query(Dish).filter_by(cuisine_id=cuisine_id).all()
    if 'username' not in login_session:
        return render_template('publicdish.html', dishes=dishes, cuisine=cuisine, creator=creator)
    elif creator.id != login_session['user_id']:
        return render_template('othersdish.html', dishes=dishes, cuisine=cuisine, creator=creator)
    else:
        return render_template('dish.html', dishes=dishes, cuisine=cuisine, creator=creator)


# Create a new dish
@app.route('/cuisine/<int:cuisine_id>/dish/new/', methods=['GET', 'POST'])
def newDish(cuisine_id):
    if 'username' not in login_session:
        return redirect('/login')
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    if login_session['user_id'] != cuisine.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add dish to this cuisine. Please create your own cuisine in order to add dishes.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newDish = Dish(name=request.form['name'], description=request.form['description'], cuisine_id=cuisine_id, user_id=cuisine.user_id)
        session.add(newDish)
        session.commit()
        flash('New Dish %s Item Successfully Created' % (newDish.name))
        return redirect(url_for('showDish', cuisine_id=cuisine_id))
    else:
        return render_template('newdish.html', cuisine_id=cuisine_id)

# Edit a dish
@app.route('/cuisine/<int:cuisine_id>/dish/<int:dish_id>/edit', methods=['GET', 'POST'])
def editDish(cuisine_id, dish_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedDish = session.query(Dish).filter_by(id=dish_id).one()
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    if login_session['user_id'] != cuisine.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit dishes to this cuisine. Please create your own cuisine in order to edit dishes.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedDish.name = request.form['name']
        if request.form['description']:
            editedDish.description = request.form['description']
        session.add(editedDish)
        session.commit()
        flash('Dish Successfully Edited')
        return redirect(url_for('showDish', cuisine_id=cuisine_id))
    else:
        return render_template('editdish.html', cuisine_id=cuisine_id, dish_id=dish_id, dish=editedDish)


# Delete a dish
@app.route('/cuisine/<int:cuisine_id>/dish/<int:dish_id>/delete', methods=['GET', 'POST'])
def deleteDish(cuisine_id, dish_id):
    if 'username' not in login_session:
        return redirect('/login')
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    dishToDelete = session.query(Dish).filter_by(id=dish_id).one()
    if login_session['user_id'] != cuisine.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete dishes to this cuisine. Please create your own cuisine in order to delete dishes.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(dishToDelete)
        session.commit()
        flash('Dish Successfully Deleted')
        return redirect(url_for('showDish', cuisine_id=cuisine_id))
    else:
        return render_template('deleteDish.html', dish=dishToDelete)

# create a new user to the database
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# get one exist user's information by ID 
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# get the user ID by email
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
