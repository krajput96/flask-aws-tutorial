from flask_wtf import Form
from wtforms import TextField, validators, SelectField, SubmitField, StringField
#from wtforms_sqlalchemy.fields import QuerySelectField


CUISINE_CHOICES = [(' ',' '), ('Mexican', 'Mexican') , ('Italian', 'Italian'), ('Indian', 'Indian'), ('French', 'French'), ('Thai', 'Thai'), ('Russian', 'Russian'), ('Spanish', 'Spanish'), ('Japanese', 'Japanese'), ('British', 'British'), ('Korean', 'Korean'), ]
CALORIES_PROTEIN_CHOICES = [(' ',' '), ('High Protein', 'High Protein'), ('Low Protein', 'Low Protein'), ('High Calories', 'High Calories'), ('Low Calories', 'Low Calories')]

class complexForm(Form):
    cuisine = SelectField(label='Cuisine: ', choices=CUISINE_CHOICES)
    calories_protein = SelectField(label='Choose: ', choices=CALORIES_PROTEIN_CHOICES)

    submit = SubmitField("Submit")

class moreInformation(Form):
    moreInfo = StringField('ID', validators = [validators.DataRequired()])
    submit = SubmitField('Submit')
