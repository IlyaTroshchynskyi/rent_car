# -*- coding: utf-8 -*-
"""config
   Implements the configuration related objects.
"""
import logging
import logging.handlers


ONE_MB = 1_000_000


def init_logger(name):
    """Init logger for application. Set formats for writing information to the files and
    for output to debug.
    Args:
        name (str): name of root logger
    """
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s ' \
             '- FUNCTION=%(funcName)s - %(message)s'
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT, datefmt='%d-%m-%Y %H:%M:%S'))
    sh.setLevel(logging.INFO)
    fh = logging.handlers.RotatingFileHandler(filename='logs/rentcars.log',
                                              maxBytes=10*ONE_MB, backupCount=100)
    fh.setFormatter(logging.Formatter(FORMAT, datefmt='%d-%m-%Y %H:%M:%S'))
    fh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.addHandler(fh)


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