# -*- coding: utf-8 -*-
"""config
   Implements the configuration related objects.
"""


class Configuration:
    """Configuration for application
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rentcars.db'
    SECRET_KEY = 'something_very_secret'
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'email'
    MAIL_PASSWORD = 'password'