from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField


class FilterForm(FlaskForm):
    classificationFilter = StringField('Classification Filter')
    submit = SubmitField('Search')
