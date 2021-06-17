import datetime
from wtforms import  FloatField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from rentcars import db
from rentcars.models import Cars, Clients, Orders
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class BaseOrder(FlaskForm):

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


class AddOrder(BaseOrder):

    car_number = QuerySelectField('Car Number', validators=[InputRequired(
        message="Data for car number have to be provided")],
            query_factory=lambda: Cars.query.all(),
                                  get_label="car_number")

    car_description = QuerySelectField('Car Description', validators=[InputRequired()],
                                       query_factory=lambda: Cars.query,
                                       get_label="car_description")
    client_passport = QuerySelectField('Client Passport', validators=[InputRequired()],
                                       query_factory=lambda: Clients.query, get_label="passport")





class UpdateOrder(BaseOrder):
    pass

