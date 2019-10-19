"""------------------------------------------------------------*-
  Form module for Flask server
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Miguel Grinberg 2018
  version 1.00 - 19/10/2019
 --------------------------------------------------------------
 *  Define the form for flask server to collect.
 *
 --------------------------------------------------------------"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from app.models import User


class InfoForm(FlaskForm):
    name = StringField('Your full name', validators=[DataRequired()])
    mssv = StringField('Your ID (MSSV)', validators=[DataRequired()])
    save = SubmitField('Save')

    def validate_mssv(self, mssv):
        if len(mssv.data)!=8:
            raise ValidationError('Wrong format. Try again.')
        user = User.query.filter_by(mssv=mssv.data).first()
        if user is not None:
            raise ValidationError('This ID existed!')
        