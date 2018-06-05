from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Book, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, flash
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Genre Books Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///genresofbookswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is {}".format(login_session['state'])
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print("access token received {} ".format(access_token))
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'.format(
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first
        index which gives us the key : value for the server access token
        then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can
        be used directly in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token={}&fields=name,id,email'.format(token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:{}".format(url)
    # print "API JSON result: {}".format(result)
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token={}&redirect=0&height=200&width=200'.format(token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # see if user exists
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
    output += """ " style = "width: 300px; height: 300px;
                  border-radius: 150px;
                  -webkit-border-radius: 150px;
                  -moz-border-radius: 150px;"> """

    flash("Now logged in as {}".format(login_session['username']))
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/{}/permissions?access_token={}'.format(
                                                   facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


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
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
           .format(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ " style = "width: 300px;
                  height: 300px;border-radius: 150px;
                  -webkit-border-radius: 150px;
                  -moz-border-radius: 150px;"> """
    flash("you are now logged in as {}".format(login_session['username']))
    print("done!")
    return output


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
                                                            access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Genre Information


@app.route('/genre/<int:genre_id>/book/JSON')
def genreBookJSON(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    items = session.query(Book).filter_by(
        genre_id=genre_id).all()
    return jsonify(Book=[i.serialize for i in items])


@app.route('/genre/<int:genre_id>/book/<int:book_id>/JSON')
def bookJSON(genre_id, book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)


@app.route('/genre/JSON')
def genresJSON():
    genres = session.query(Genre).all()
    return jsonify(genres=[g.serialize for g in genres])


# Show all genres
@app.route('/')
@app.route('/genre/')
def showGenres():
    genres = session.query(Genre).order_by(asc(Genre.name))
    if 'username' not in login_session:
        return render_template('publicGenres.html', genres=genres)
    else:
        return render_template('genres.html', genres=genres)

# Create a new genre


@app.route('/genre/new/', methods=['GET', 'POST'])
def newGenre():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newGenre = Genre(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newGenre)
        flash("New Genre '{}' Successfully Created".format(newGenre.name))
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('newGenre.html')

# Edit a genre


@app.route('/genre/<int:genre_id>/edit/', methods=['GET', 'POST'])
def editGenre(genre_id):
    editedGenre = session.query(
        Genre).filter_by(id=genre_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedGenre.user_id != login_session['user_id']:
        return """<script>function myFunction(){
               alert('You are not authorized to edit this genre
               as you have not created it.');
               }</script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
            flash("Successfully edited '{}'".format(editedGenre.name))
            return redirect(url_for('showGenres'))
    else:
        return render_template('editGenre.html', genre=editedGenre)


# Delete a genre
@app.route('/genre/<int:genre_id>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    genreToDelete = session.query(
        Genre).filter_by(id=genre_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if genreToDelete.user_id != login_session['user_id']:
        return """<script>function myFunction(){
               alert('You are not authorized to delete
               this genre as you have not created it.');
               }</script><body onload='myFunction()''>"""
    if request.method == 'POST':
        session.delete(genreToDelete)
        flash("Successfully deleted '{}'".format(genreToDelete.name))
        session.commit()
        return redirect(url_for('showGenres', genre_id=genre_id))
    else:
        return render_template('deleteGenre.html', genre=genreToDelete)

# Show a genre books


@app.route('/genre/<int:genre_id>/')
@app.route('/genre/<int:genre_id>/books/')
def showBooks(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    creator = getUserInfo(genre.user_id)
    books = session.query(Book).filter_by(
        genre_id=genre_id).all()
    if 'username' not in login_session or creator.id != login_session[
                                                            'user_id']:
        return render_template('publicBooks.html',
                               books=books, genre=genre, creator=creator)
    else:
        return render_template('books.html',
                               books=books, genre=genre, creator=creator)


# Create a new book
@app.route('/genre/<int:genre_id>/books/new/', methods=['GET', 'POST'])
def newBook(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if login_session['user_id'] != genre.user_id:
        return """<script>function myFunction(){
               alert('You are not authorized to add books
               to this genre as you have not created it.');
               }
               </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        newBook = Book(picture=request.form['picture'],
                       name=request.form['name'],
                       author=request.form['author'],
                       description=request.form['description'],
                       price=request.form['price'],
                       rating=request.form['rating'],
                       genre_id=genre_id,
                       user_id=genre.user_id)
        session.add(newBook)
        session.commit()
        flash("New Book '{}' Successfully Created".format(newBook.name))
        return redirect(url_for('showBooks', genre_id=genre_id))
    else:
        return render_template('newbook.html', genre_id=genre_id)

# Edit a book


@app.route('/genre/<int:genre_id>/books/<int:book_id>/edit',
           methods=['GET', 'POST'])
def editBook(genre_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedBook = session.query(Book).filter_by(id=book_id).one()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if login_session['user_id'] != genre.user_id:
        return """<script>function myFunction(){
        alert('You are not authorized to edit books in this genre.
             as you have not created it.');
        }
        </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['picture']:
            editedBook.picture = request.form['picture']
        if request.form['name']:
            editedBook.name = request.form['name']
        if request.form['author']:
            editedBook.author = request.form['author']
        if request.form['description']:
            editedBook.description = request.form['description']
        if request.form['price']:
            editedBook.price = request.form['price']
        if request.form['rating']:
            editedBook.rating = request.form['rating']
        session.add(editedBook)
        session.commit()
        flash("Successfully edited '{}'".format(editedBook.name))
        return redirect(url_for('showBooks', genre_id=genre_id))
    else:
        return render_template('editBook.html',
                               genre_id=genre_id,
                               book_id=book_id,
                               book=editedBook)


# Delete a book
@app.route('/genre/<int:genre_id>/books/<int:book_id>/delete',
           methods=['GET', 'POST'])
def deleteBook(genre_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(id=genre_id).one()
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    if login_session['user_id'] != genre.user_id:
        return """<script>function myFunction(){
               alert('You are not authorized to delete books in this genre.
                     as you have not created it.');
                     }
               </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        flash("Successfully deleted '{}'".format(bookToDelete.name))
        return redirect(url_for('showBooks',
                                genre_id=genre_id,
                                book_id=book_id))
    else:
        return render_template('deleteBook.html',
                               book=bookToDelete,
                               book_id=book_id,
                               genre_id=genre_id)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['access_token']
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showGenres'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showGenres'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
