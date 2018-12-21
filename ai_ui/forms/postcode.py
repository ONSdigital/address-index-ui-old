from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, validators, IntegerField


class PostcodeForm(FlaskForm):
    postcode = StringField('Postcode', [validators.DataRequired("Please enter a postcode.")])
    classificationFilter = StringField('Classification Filter')
    historical = RadioField('Include historical data?', [validators.DataRequired()],
                            choices=[('true', 'Yes'), ('false', 'No')], default='true')
    resultsPerPage = IntegerField('Results per page')
    submit = SubmitField('Search')
