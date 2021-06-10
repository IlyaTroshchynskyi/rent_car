class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/rentcars'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rentcars.db'
    SECRET_KEY = 'something_very_secret'
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'