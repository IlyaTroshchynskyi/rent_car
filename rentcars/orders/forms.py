# -*- coding: utf-8 -*-
"""forms
   Implements the forms for orders
"""
import datetime
from wtforms import FloatField
from wtforms.validators import InputRequired, NumberRange, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from rentcars.models import Cars, Clients, Orders


class BaseOrder(FlaskForm):
    """Base form for avoiding duplicate fields
    """

    order_date = DateField('Order Date', validators=[InputRequired()])
    rental_time = FloatField('Rental Time', validators=[InputRequired(),
                NumberRange(min=1, message="Minimal value is one day")])

    def validate_order_date(form, order_date):
        """Validate order date. If order date less current then raise Validation error.
        Args:
            order_date (datetime): Date
        Raises:
            ValidationError
        """
        if not order_date.data >= datetime.date.today():
            raise ValidationError('The day must be no less then current')

    def validate_car_number(form, field):
        """Validate car number. Car number must exist in database or not been taken in
        day of the order.
        Args:
            field (str): Car number
        Raises:
            ValidationError
        """
        car = Cars.query.filter_by(car_number=field.data.car_number).first()
        order = Orders.query.filter_by(car_number=field.data.car_number).first()
        if car is None or \
                (order and order.car_number == field.data.car_number
                 and order.date_rent.date() == form.order_date.data):
            raise ValidationError('This cars is unavailable for that day '
                                  'or not in database')

    def validate_car_description(form, field):
        """Validate car description. Car description must be equal description of the car
        from the database.
        Args:
            field (str): Car description
        Raises:
            ValidationError
        """
        car = Cars.query.filter_by(car_number=form.car_number.data.
                                   car_number).first()
        if field.data.car_description != car.car_description:
            raise ValidationError('The description must be match'
                                  ' with cars number')


class AddOrder(BaseOrder):
    """Form for adding new orders or updating orders
    """

    car_number = QuerySelectField('Car Number', validators=[InputRequired(
        message="Data for cars number have to be provided")],
                                  query_factory=lambda: Cars.query.all,
                                  get_label="car_number")

    car_description = QuerySelectField('Car Description',
                                       validators=[InputRequired()],
                                       query_factory=lambda: Cars.query,
                                       get_label="car_description")
    client_passport = QuerySelectField('Client Passport',
                                       validators=[InputRequired()],
                                       query_factory=lambda: Clients.query,
                                       get_label="passport")
