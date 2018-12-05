from flask_wtf import FlaskForm

from wtforms import TextField, RadioField, SubmitField

from wtforms import validators, ValidationError


class postcodeForm(FlaskForm):
    postcode = TextField('Postcode', [validators.DataRequired("Please enter a postcode.")])
    classificationFilter = TextField('Classification Filter')
    historical = RadioField('Include historical data?', [validators.Required()], choices=[('true','Yes'),('false','No')], default='true')
    resultsPerPage = TextField('Results per page', default='10')
    submit = SubmitField('Search')

class addressForm(FlaskForm):
    address = TextField('Address', [validators.Required("Please enter an address.")])
    classificationFilter = TextField('Classification Filter')
    historical = RadioField('Include historical data?', [validators.Required()], choices=[('true','Yes'),('false','No')], default='true')
    resultsPerPage = TextField('Results per page', default='10')
    submit = SubmitField('Search')

