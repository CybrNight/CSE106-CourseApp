from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from flask import make_response
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from project.role import Role
from . import db
import uuid
from functools import wraps

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('auth.login'))

        # if the above check passes, then we know the user has the right
        # credentials
        login_user(user, remember=remember)

        if user.role == Role.ADMIN:
            return (redirect("/admin"))
        return redirect(url_for("main.index"))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        # code to validate and add user to database goes here
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        user_id = uuid.uuid4().hex[:8]
        exists = db.session.query(User.user_id).filter_by(
            user_id=user_id).first() is not None

        while exists:
            user_id = uuid.uuid4().hex[:8]
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name,
                        password=password, user_id=user_id)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("main.index"))
