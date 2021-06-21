# -*- coding: utf-8 -*-
"""routes
   Implements the routes blueprint users.
"""
from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from rentcars.users.forms import RegistrationForm, LoginForm
from rentcars import db
from rentcars.models import User


users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """Register new users. Validate data in the form. Hashes the
    password for security. After registration redirect to login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('orders.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are able to log in',
              'success')
        return redirect(url_for('users.login_page'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login_user",  methods=['GET', 'POST'])
def login_page():
    """Login users. Validate data in the form.
     After login redirect to index page
    """
    if current_user.is_authenticated:
        return redirect(url_for('orders.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else \
                redirect(url_for('orders.index'))

        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('security/login_user.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """Logs user out.
    """
    logout_user()
    return redirect(url_for('orders.index'))
