from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange
from flask_wtf import FlaskForm


class AddCar(FlaskForm):

    car_number = StringField('Car Number', validators=[InputRequired(
        message="Data for car number have to be provided")])
    car_description = StringField('Car Description', validators=[InputRequired(),
        Length(min=3, max=90, message="Car description have to be from 3 to 90 characters")])
    rental_cost = FloatField('Rental Cost', validators=[InputRequired(),
        NumberRange(min=1, message="Should contain numbers from 1")])