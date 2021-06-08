from wtforms import Form, StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField


class AddOrder(Form):

    car_number = StringField('car number', validators=[InputRequired(
        message="Data for car number have to be provided")])
    car_description = StringField('car description', validators=[InputRequired()])
    client_passport = StringField('client passport', validators=[InputRequired(),
        Length(min=4, max=90, message="The name have to be from 5 to 90 characters")])
    client_name = StringField('client name', validators=[InputRequired()])
    order_date = DateField('order date', validators=[InputRequired()])
    rental_time = FloatField('rental time', validators=[InputRequired()])
