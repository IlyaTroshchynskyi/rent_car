from datetime import datetime
from rentcars import db


class Orders(db.Model):

    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column(db.String(10))
    car_description = db.Column(db.String(50), nullable=False)
    client_passport = db.Column(db.String(10))
    date_rent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rental_time = db.Column(db.Integer, nullable=False)
    rental_cost = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    car = db.relationship('Cars', backref='cars', lazy=True)
    clients = db.relationship('Clients', backref='clients', lazy=True)


class Cars(db.Model):

    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column(db.String(10), db.ForeignKey('orders.car_number'), unique=True)
    car_description = db.Column(db.String(50), nullable=False)
    rental_cost = db.Column(db.Float)
    number_orders = db.Column(db.Integer, default=0)


class Clients(db.Model):

    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    passport = db.Column(db.String(10), db.ForeignKey('orders.client_passport'), unique=True)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    number_orders = db.Column(db.Integer, default=0)
