from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, validators


class AddressForm(FlaskForm):
    address = StringField('Address', [validators.DataRequired("Please enter an address.")])
    classificationFilter = StringField('Classification Filter')
    historical = RadioField('Include historical data?', [validators.DataRequired()],
                            choices=[('true', 'Yes'), ('false', 'No')], default='true')
    resultsPerPage = StringField('Results per page', default='10')
    submit = SubmitField('Search')
