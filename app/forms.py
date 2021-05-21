from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, Form, SelectField
from wtforms.fields.core import BooleanField, FieldList, FormField
from wtforms.validators import InputRequired, EqualTo, Email, ValidationError
from wtforms.fields.html5 import DateTimeLocalField
from app.models import ProctorSession

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
    disable_eye_detection = BooleanField("Disable Eye Detection ?")
    email = StringField("Enter Email", validators=[InputRequired(),Email()])

class ProctorSessionForm(FlaskForm):
    session_name = StringField("Session Name", validators=[InputRequired()])
    start_time = DateTimeLocalField("Start Time",format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    end_time = DateTimeLocalField("End Time",format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    session_users = FieldList(FormField(SessionUserForm), min_entries=2)
    submit = SubmitField("Create!")

    def validate_session_name(form, field):
        session_name = field.data
        if ProctorSession.query.filter_by(name=session_name).first():
            raise ValidationError("Name Taken, choose another")        
    
class ExamQuestionForm(Form):
    question = StringField("Enter Question Text", validators=[InputRequired()])

class ExamFormForm(FlaskForm):
    proctor_id = SelectField("Proctor Session",coerce=int, validators=[InputRequired()])
    exam_questions = FieldList(FormField(ExamQuestionForm), min_entries=2)
    submit = SubmitField("Create Exam Form")

    



