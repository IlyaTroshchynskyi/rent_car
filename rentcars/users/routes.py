from flask import Blueprint, redirect, url_for, render_template, flash, request
from rentcars.users.forms import RegistrationForm, LoginForm
from flask_login import current_user, logout_user, login_user
# from flask_security import roles_accepted, roles_required,login_user, current_user, logout_user
from rentcars import db
from werkzeug.security import generate_password_hash, check_password_hash
from rentcars.models import User


users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('orders.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are able to log in', 'success')
        return redirect(url_for('users.login_page'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login_user",  methods=['GET', 'POST'])
def login_page():
    print(current_user)
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('orders.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('orders.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('security/login_user.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('orders.index'))

