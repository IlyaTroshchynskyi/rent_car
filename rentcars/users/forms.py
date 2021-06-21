# -*- coding: utf-8 -*-
"""forms
   Implements the forms for users
"""
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField,\
    BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from rentcars.models import User


class RegistrationForm(FlaskForm):
    """Form for registration users
    """

    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=5, max=50)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """ Validate username. If username exist then raise Validation error.
        Username must be unique
        Args:
            username (str): Username
        Raises:
            ValidationError
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. '
                                  'Please choose other one')

    def validate_email(self, email):
        """ Validate username. If email exist then raise Validation error.
        Email must be unique
        Args:
            email (str): Email
        Raises:
            ValidationError
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. '
                                  'Please choose other one')


class LoginForm(FlaskForm):
    """Form for login users
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
