import datetime
from wtforms import  FloatField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from rentcars import db
from rentcars.models import Cars, Clients, Orders
from wtforms.ext.sqlalchemy.fields import QuerySelectField
# name=QuerySelectField('Name',query_factory=lambda:A.query,get_label="username")
# def car_choices():
#     return  db.session.query(Cars.car_number).all()
# def car_choices():
#     return  db.session.query(Cars).all()
# def car_description():
#     return [car.car_description for car in db.session.query(Cars).all()]
#
# def client_passport():
#     return [car.car_description for car in db.session.query(Clients).all()]

class AddOrder(FlaskForm):
    # car_number = SelectField('Car Number' )

    car_number = QuerySelectField('Car Number', validators=[InputRequired(
        message="Data for car number have to be provided")],
            query_factory=lambda: Cars.query.all(), get_label="car_number", blank_text="Click to select")

    car_description = QuerySelectField('Car Description', validators=[InputRequired()]
                                       ,query_factory=lambda: Cars.query, get_label="car_description")
    client_passport = QuerySelectField('Client Passport', validators=[InputRequired()],

        query_factory=lambda: Clients.query, get_label="passport")
    order_date = DateField('Order Date', validators=[InputRequired()])
    rental_time = FloatField('Rental Time', validators=[InputRequired(),
        NumberRange(min=1, message="Minimal value is one day")])

    def validate_order_date(form, field):
        if not field.data >= datetime.date.today():
            raise ValidationError('The day must be no less then current')

    def validate_car_number(form, field):
        car = Cars.query.filter_by(car_number=field.data.car_number).first()
        order = Orders.query.filter_by(car_number=field.data.car_number).first()
        if car is None or (order and order.car_number == field.data.car_number \
                and order.date_rent.date() == form.order_date.data):
            raise ValidationError('This car is unavailable for that day or not in database')

    def validate_car_description(form, field):
        car = Cars.query.filter_by(car_number=form.car_number.data.car_number).first()
        if field.data.car_description != car.car_description:
            raise ValidationError('The description must be match with car number')


# class AddOrder(FlaskForm):
#     # car_number = SelectField('Car Number' )
#
#     car_number = QuerySelectField('Car Number', validators=[InputRequired(
#         message="Data for car number have to be provided")],
#                                   query_factory=lambda: Cars.query.all(), get_label="car_number", blank_text="Click to select")
#
#     car_description = QuerySelectField('Car Description', validators=[InputRequired(),
#         Length(min=1, max=90, message="Car description have to be from 3 to 90 characters")],
#                                        query_factory=lambda: Cars.query, get_label="car_description")
#     client_passport = QuerySelectField('Client Passport', validators=[InputRequired(),
#         Length(min=4, max=10, message="The passport have to be from 4 to 10 characters")],
#         query_factory=lambda: Clients.query, get_label="passport")
#     order_date = DateField('Order Date', validators=[InputRequired()])
#     rental_time = FloatField('Rental Time', validators=[InputRequired(),
#         NumberRange(min=1, message="Minimal value is one day")])