from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField

from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf

class AddPet(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    species = StringField("Species", validators=[InputRequired(), AnyOf(values=["dog", "cat", "porcupine"], message="Only accepting dogs, cats, and porcupines")])
    photo_url = StringField("Picture URL", validators=[Optional(), URL(message="Not a valid URL")])
    age = FloatField("Age in years", validators=[Optional(), NumberRange(min=0, max=30, message="Number must be between 0-30")])
    notes = StringField("Any notes?", validators=[Optional()])
    available = SelectField("Currently Available", choices=[(True, 'Yes, available'), ('', 'No, not available')])