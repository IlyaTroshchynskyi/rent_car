import datetime
from wtforms import StringField
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from rentcars.models import Clients


class AddClient(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(),
        Length(min=3, max=90, message="First name have to be from 3 to 45 characters")])
    last_name = StringField('Last name', validators=[InputRequired(),
        Length(min=3, max=90, message="Last name have to be from 3 to 45 characters")])
    client_passport = StringField('Client Passport', validators=[InputRequired(),
        Length(min=4, max=10, message="The passport have to be from 4 to 10 characters")])
    register_date = DateField('Register Date', validators=[InputRequired()])

    def validate_register_date(form, field):
        if not field.data >= datetime.date.today():
            raise ValidationError('The day must be no less then current')

    def validate_client_passport(form, field):
        car = Clients.query.filter_by(passport=field.data).first()
        if car is not None:
            raise ValidationError('This client is exist in database')