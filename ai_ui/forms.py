from flask_wtf import FlaskForm

from wtforms import StringField, RadioField, SubmitField

from wtforms import validators


class PostcodeForm(FlaskForm):
    postcode = StringField('Postcode', [validators.DataRequired("Please enter a postcode.")])
    classificationFilter = StringField('Classification Filter')
    historical = RadioField('Include historical data?', [validators.DataRequired()],
                            choices=[('true', 'Yes'), ('false', 'No')], default='true')
    resultsPerPage = StringField('Results per page', default='10')
    submit = SubmitField('Search')


class UPRNForm(FlaskForm):
    uprn = StringField('UPRN', [validators.DataRequired("Please enter a UPRN.")])
    historical = RadioField('Include historical data?', [validators.DataRequired()],
                            choices=[('true', 'Yes'), ('false', 'No')], default='true')
    submit = SubmitField('Search')


class AddressForm(FlaskForm):
    address = StringField('Address', [validators.DataRequired("Please enter an address.")])
    classificationFilter = StringField('Classification Filter')
    historical = RadioField('Include historical data?', [validators.DataRequired()],
                            choices=[('true', 'Yes'), ('false', 'No')], default='true')
    resultsPerPage = StringField('Results per page', default='10')
    submit = SubmitField('Search')


class FilterForm(FlaskForm):
    classificationFilter = StringField('Classification Filter')
    submit = SubmitField('Search')
