from flask_wtf import Form
from wtforms import TextField, validators, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField


CUISINE_CHOICES = [(' ',' '), ('Mexican', 'Mexican') , ('Italian', 'Italian'), ('Indian', 'Indian')]

CALORIES_CHOICES = [(' ',' '), ('High Calories', 'High Calories'), ('Low Calories', 'Low Calories')]

PROTEIN_CHOICES = [(' ',' '), ('High Protein', 'High Protein'), ('Low Protein', 'Low Protein')]

CALORIES_PROTEIN_CHOICES = [(' ',' '), ('High Protein', 'High Protein'), ('Low Protein', 'Low Protein'), ('High Calories', 'High Calories'), ('Low Calories', 'Low Calories')]

class cuisineForm(Form):
    cuisine = SelectField(label='Cuisine', choices=CUISINE_CHOICES)
    submit = SubmitField("Submit")

class caloriesForm(Form):
    calories = SelectField(label='Calories', choices=CALORIES_CHOICES)
    submit = SubmitField("Submit")

class complexForm(Form):
    cuisine = SelectField(label='Cuisine', choices=CUISINE_CHOICES)
    calories_protein = SelectField(label='Calories', choices=CALORIES_PROTEIN_CHOICES)

    submit = SubmitField("Submit")
