from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired("Please enter your username.")])
    password = StringField('Password', [validators.DataRequired("Please enter your password.")])
    submit = SubmitField('Sign in')
