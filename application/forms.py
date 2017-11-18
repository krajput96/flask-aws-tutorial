from flask_wtf import Form
from wtforms import TextField, validators, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField


CUISINE_CHOICES = [('Mexican', 'Mexican') , ('Italian', 'Italian'), ('Indian', 'Indian')]


class cuisineForm(Form):
    cuisine = SelectField(label='Cuisine', choices=CUISINE_CHOICES)
    submit = SubmitField("Submit")
