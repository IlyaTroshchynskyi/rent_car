import datetime
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from models import Cars, Orders


class AddOrder(FlaskForm):

    car_number = StringField('car number', validators=[InputRequired(
        message="Data for car number have to be provided")])
    car_description = StringField('car description', validators=[InputRequired(),
        Length(min=3, max=90, message="Minimum length 3 maximum length of 90 characters")])
    client_passport = StringField('client passport', validators=[InputRequired(),
        Length(min=4, max=90, message="The name have to be from 5 to 90 characters")])
    client_name = StringField('client name', validators=[InputRequired()])
    order_date = DateField('order date', validators=[InputRequired()])
    rental_time = FloatField('rental time', validators=[InputRequired(),
        NumberRange(min=1, message="Minimal value is one day")])

    submit = SubmitField('Add Order')

    def validate_order_date(form, field):
        if not field.data > datetime.date.today():
            raise ValidationError('The day must be no less then current')

    def validate_car_number(form, field):
        car = Cars.query.filter_by(car_number=field.data).first()
        print(car)
        order = Orders.query.filter_by(car_number=field.data).first()
        if car is None or (order and order.car_number == field.data \
                and order.date_rent.date() == form.order_date.data):
            raise ValidationError('This car is unavailable for that day or not in database')


class AddCar(FlaskForm):

    car_number = StringField('car number', validators=[InputRequired(
        message="Data for car number have to be provided")])
    car_description = StringField('car description', validators=[InputRequired(),
        Length(min=3, max=90, message="Minimum length 3 maximum length of 90 characters")])
    rental_cost = FloatField('rental cost', validators=[InputRequired(),
        NumberRange(min=1, message="Minimal value is one day")])


    submit = SubmitField('Add Car')


class AddClient(FlaskForm):
    first_name = StringField('first name', validators=[InputRequired(
        message="Data for car number have to be provided")])
    last_name = StringField('last name', validators=[InputRequired(),
        Length(min=3, max=90, message="Minimum length 3 maximum length of 90 characters")])
    client_passport = StringField('client passport', validators=[InputRequired(),
        Length(min=4, max=90, message="The name have to be from 5 to 90 characters")])
    register_date = DateField('order date', validators=[InputRequired()])
    submit = SubmitField('Add Client')

    def validate_register_date(form, field):
        if not field.data > datetime.date.today():
            raise ValidationError('The day must be no less then current')