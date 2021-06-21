# -*- coding: utf-8 -*-
"""forms
   Implements the forms for cars
"""
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError
from flask_wtf import FlaskForm
from rentcars.models import Cars


class AddCar(FlaskForm):
    """Form for adding new car to database or updating information about car
    """

    car_number = StringField('Car Number', validators=[InputRequired(
        message="Data for cars number have to be provided")])
    car_description = StringField('Car Description', validators=[InputRequired(),
        Length(min=3, max=90, message="Car description have to be from 3 to 90 characters")])
    rental_cost = FloatField('Rental Cost', validators=[InputRequired(),
        NumberRange(min=1, message="Should contain numbers from 1")])

    def validate_car_number(form, field):
        """Validate car number. Car number must be unique
        Args:
            field (str): Car number
        Raises:
            ValidationError
        """
        car = Cars.query.filter_by(car_number=field.data).first()
        if car is not None:
            raise ValidationError('This cars is exist in database')