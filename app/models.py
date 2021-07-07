from sqlalchemy.orm import backref
from flask import current_app
from app import db, login, tokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
@login.user_loader
def load_user(id):
    return User.query.get(int(id)) or SessionUser.query.get(int(id))

@tokenAuth.verify_token
def verify_token(token):
    user = SessionUser.verify_auth_token(token)
    if user == "TOKEN_EXPIRE":
        return None
    elif user == "TOKEN_BAD":
        return None
    else:
        return user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    proctor_sessions = db.relationship("ProctorSession", backref="user_id", lazy='dynamic')
    exam_forms = db.relationship("ExamForm", backref="user_id", lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "< User {}>".format(self.username)


class ProctorSession(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), unique=True, index=True, nullable=False)
    start_time = db.Column(db.DateTime(timezone=True),nullable=False)
    end_time = db.Column(db.DateTime(timezone=True), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    parent_user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    exam_form = db.relationship("ExamForm", backref="proctor_session", lazy='dynamic')
    session_users = db.relationship("SessionUser", backref="proctor_session", lazy='dynamic' )

    def __repr__(self):
        return (" -{id}- {name} \t\n from {start} to {end} , {seconds}s. ".format(id=(self.id or "ID"), name=self.name,start=self.start_time, end=self.end_time, seconds=self.duration))

class SessionUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    token = db.Column(db.String(), nullable=False)
    details = db.Column(db.JSON(), default="\{\}")
    id_card = db.Column(db.String(), nullable=True)
    submitted = db.Column(db.Boolean(), nullable=False, default=False)
    proctor_id = db.Column(db.Integer, db.ForeignKey('proctor_session.id'))
    exam_response = db.relationship("ExamResponse", backref="session_user_id", uselist=False)

    def generate_auth_token(self, duration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = duration)
        self.token = s.dumps({'id':self.id}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            print(data)
        except SignatureExpired:
            return "TOKEN_EXPIRE"
        except BadSignature:
            return "TOKEN_BAD"
        user = SessionUser.query.get(data['id'])
        return user
    
    def __repr__(self):
        return (" -{id}-   {name}\n\t{email}\n\t{token}\n\t{proctor_id} ".format(id=self.id or "ID",name=self.name, email=self.email, token=self.token, proctor_id=self.proctor_id))


class ExamForm(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    form_description = db.Column(db.JSON(), nullable=False, default="{}")
    parent_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    proctor_id = db.Column(db.Integer, db.ForeignKey("proctor_session.id"))
    exam_responses = db.relationship("ExamResponse", backref="exam_form", lazy='dynamic')

    def __repr__(self):
        return f' - {self.id}  {self.form_description}'

class ExamResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    response = db.Column(db.JSON(), nullable=False)
    examinee_id = db.Column(db.Integer, db.ForeignKey("session_user.id"))
    exam_form_id = db.Column(db.Integer, db.ForeignKey("exam_form.id"))

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proctoring_logs = db.Column(db.JSON(), nullable=False)
    