from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user
from authlib.integrations.flask_client import OAuth
import requests
from . import db
import sys


GOOGLE_CLIENT_ID = '384697585082-kntjgh746jsfm3tj26n2ol27ev7vpp76.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
CONF_URL = GOOGLE_DISCOVERY_URL


auth = Blueprint('auth', __name__)

oauth = OAuth(current_app)
oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    """
    Grabs login form details, verifies credentials, and redirects the user to profile on successful submission 
    """
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))

@auth.route('/google')
def google():
    # Redirect to google_auth function
    redirect_uri = url_for('auth.google_auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@auth.route('/google/auth')
def google_auth():
    # Auth with google
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, token['userinfo']['nonce'])
    print(" Google User: {}".format(user), file=sys.stderr)
    # Register if new user
    user = User.query.filter_by(email=token['userinfo']['email']).first()
    if not user:
        new_user = User(email=token['userinfo']['email'], name=token['userinfo']['name'])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=False)
    else:
        # Login
        login_user(user, remember=False)

    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    """
    Grabs signup form details, checks for new user, adds new user to DB if new, redirect to login 
    """
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    password_match = (password == password_confirm)

    if not password_match: # if password dont match, user is found we want to redirect back to signup page so user can try again
        flash('Passwords do not match')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.signup_success'))


@auth.route('/signup_success')
def signup_success():
    return render_template('signup_success.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))