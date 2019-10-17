from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class InfoForm(FlaskForm):
    name = StringField('Your full name', validators=[DataRequired()])
    mssv = StringField('Your ID (MSSV)', validators=[DataRequired()])
    save = SubmitField('Save')
