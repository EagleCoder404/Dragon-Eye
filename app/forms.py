from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, Form,HiddenField
from wtforms.fields.core import FieldList, FormField
from wtforms.validators import InputRequired, EqualTo, Email
from wtforms.widgets.core import Input
from wtforms.fields.html5 import DateTimeLocalField


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Enter Password', validators=[InputRequired()])
    confirm = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password', 'Password should Match!')])
    email = StringField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Register!")

class SessionUserForm(Form):
    username = StringField("Enter Name", validators=[InputRequired()])
    email = StringField("Enter Email", validators=[InputRequired(),Email()])

class ProctorSessionForm(FlaskForm):
    session_name = StringField("Session Name", validators=[InputRequired()])
    start_time = DateTimeLocalField("Start Time",format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    end_time = DateTimeLocalField("End Time",format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    session_users = FieldList(FormField(SessionUserForm), min_entries=2)
    submit = SubmitField("Create!")

    



