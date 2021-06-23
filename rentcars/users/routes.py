# -*- coding: utf-8 -*-
"""routes
   Implements the routes blueprint users.
"""
from flask import Blueprint, redirect, url_for, render_template, flash, request, current_app
from flask_login import current_user, logout_user, login_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from rentcars.users.forms import RegistrationForm, LoginForm, RequestResetForm,\
    ResetPasswordForm
from rentcars import db, mail
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


@users.route("/reset_password",  methods=['GET', 'POST'])
def reset_request():
    """Send the letter with token to the email for changing password.
     If token expires then you need to re-send a message to the mail
    """
    if current_user.is_authenticated:
        return redirect(url_for('orders.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>",  methods=['GET', 'POST'])
def reset_token(token):
    """ Check if token doesn't expires
    """
    if current_user.is_authenticated:
        return redirect(url_for('orders.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are able to log in', 'success')
        return redirect(url_for('users.login_page'))
    return render_template('reset_token.html', title='Request Password', form=form)


def send_reset_email(user):
    """Send the message to user for resetting password
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f""" To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no change
    """
    mail.send(msg)