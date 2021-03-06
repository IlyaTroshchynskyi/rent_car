# -*- coding: utf-8 -*-
"""models
   Implements the models for database tables.
"""
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,\
    SignatureExpired
from flask_security import UserMixin, RoleMixin
from flask import current_app
from rentcars import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Reload the user object from the user ID stored in the session
    Args:
        user_id (str): User id
    Returns:
        user (obj): User
    """
    return User.get(int(user_id))


class Orders(db.Model):
    """Table for saving orders of clients
    """

    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column(db.String(10), db.ForeignKey('cars.car_number'))
    car_description = db.Column(db.String(50), nullable=False)
    client_passport = db.Column(db.String(10),
                                db.ForeignKey('clients.passport'))
    date_rent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rental_time = db.Column(db.Integer, nullable=False)
    rental_cost = db.Column(db.Float)
    total_cost = db.Column(db.Float)


class Cars(db.Model):
    """Table for saving cars
    """

    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column(db.String(10), unique=True)
    car_description = db.Column(db.String(50), nullable=False)
    rental_cost = db.Column(db.Float)
    number_orders = db.Column(db.Integer, default=0)
    order = db.relationship('Orders', backref='cars', lazy=True)

    def __repr__(self):
        return self.car_number


class Clients(db.Model):
    """Table for saving clients
    """

    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    passport = db.Column(db.String(10), unique=True)
    register_date = db.Column(db.DateTime, nullable=False,
                              default=datetime.utcnow)
    number_orders = db.Column(db.Integer, default=0)
    order = db.relationship('Orders', backref='client', lazy=True)

    def __repr__(self):
        return self.passport


roles_user = db.Table('roles_user', db.Column('user_id',
                                              db.Integer(),
                                              db.ForeignKey('user.id')),
                      db.Column('role_id',
                                db.Integer(),
                                db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    """Table for saving users who work with this app. Have relationships
     with table role many-to-many
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_user,
                            backref=db.backref('users', lazy='dynamic'))

    def get_reset_token(self, expires_sec=1800):
        """Help to change password using token
        Returns:
            token (str): Token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """Check if token doesn't expired
        Args:
            token (str): Token
        Returns:
            user (obj): User
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except SignatureExpired:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return self.username


class Role(db.Model, RoleMixin):
    """Table for saving roles of users. Have relationships with table user
    many-to-many
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name
