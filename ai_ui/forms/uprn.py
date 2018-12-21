from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, validators


class UPRNForm(FlaskForm):
    uprn = StringField('UPRN', [validators.DataRequired("Please enter a UPRN.")])
    historical = RadioField('Include historical data?', [validators.DataRequired()],
                            choices=[('true', 'Yes'), ('false', 'No')], default='true')
    submit = SubmitField('Search')
