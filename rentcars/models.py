from app import db
from datetime import datetime


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column(db.String(10), unique=True)
    client_passport = db.Column(db.String(10), unique=True)
    date_rent = db.Column(db.DateTime, nullable=False, default=datetime.now())
    rental_time = db.Column(db.Integer, nullable=False)
    rental_cost = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    car = db.relationship('Cars', backref='order_cars', lazy=True)
    # clients = db.relationship('Clients', backref='clients', lazy=True)


# class Clients(db.Model):
#     client_passport = db.Column(db.String(10), db.ForeignKey('orders.client_passport'),
#                                 primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     registration_date = db.Column(db.DateTime, default=datetime.now())
#     my_orders = db.relationship()

 # order1 = Orders(car_number="AX333333",client_passport="AH444444",rental_time=4,rental_cost=45,total_cost=180)
class Cars(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column(db.String(10), db.ForeignKey('orders.car_number'), unique=True)

    car_description = db.Column(db.String(50), nullable=False)
    rental_cost = db.Column(db.Float)
    count_orders = db.Column(db.Integer)

