import datetime
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError, Regexp
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from models import Cars, Orders


class AddOrder(FlaskForm):

    car_number = StringField('Car Number', validators=[InputRequired(
        message="Data for car number have to be provided")])
    car_description = StringField('Car Description', validators=[InputRequired(),
        Length(min=1, max=90, message="Car description have to be from 3 to 90 characters")])
    client_passport = StringField('Client Passport', validators=[InputRequired(),
        Length(min=4, max=10, message="The passport have to be from 4 to 10 characters")])
    order_date = DateField('Order Date', validators=[InputRequired()])
    rental_time = FloatField('Rental Time', validators=[InputRequired(),
        NumberRange(min=1, message="Minimal value is one day")])

    submit = SubmitField('Add Order')

    def validate_order_date(form, field):
        if not field.data >= datetime.date.today():
            raise ValidationError('The day must be no less then current')

    def validate_car_number(form, field):
        car = Cars.query.filter_by(car_number=field.data).first()
        order = Orders.query.filter_by(car_number=field.data).first()
        if car is None or (order and order.car_number == field.data \
                and order.date_rent.date() == form.order_date.data):
            raise ValidationError('This car is unavailable for that day or not in database')


class AddCar(FlaskForm):

    car_number = StringField('Car Number', validators=[InputRequired(
        message="Data for car number have to be provided")])
    car_description = StringField('Car Description', validators=[InputRequired(),
        Length(min=3, max=90, message="Car description have to be from 3 to 90 characters")])
    rental_cost = FloatField('Rental Cost', validators=[InputRequired(),
        NumberRange(min=1, message="Should contain numbers from 1")])
    submit = SubmitField('Add Car')


class AddClient(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(),
        Length(min=3, max=90,message="First name have to be from 3 to 45 characters")])
    last_name = StringField('Last name', validators=[InputRequired(),
        Length(min=3, max=90, message="Last name have to be from 3 to 45 characters")])
    client_passport = StringField('Client Passport', validators=[InputRequired(),
        Length(min=4, max=10, message="The passport have to be from 4 to 10 characters")])
    register_date = DateField('Register Date', validators=[InputRequired()])
    submit = SubmitField('Add Client')

    def validate_register_date(form, field):
        if not field.data >= datetime.date.today():
            raise ValidationError('The day must be no less then current')