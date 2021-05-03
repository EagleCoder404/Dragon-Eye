from sqlalchemy.orm import backref
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) or SessionUser.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    proctor_sessions = db.relationship("ProctorSession", backref="user_id", lazy='dynamic')
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
    session_users = db.relationship("SessionUser", backref="proctor_session", lazy='dynamic' )

    def __repr__(self):
        return (" -{id}- {name} \t\n from {start} to {end} , {seconds}s. ".format(id=(self.id or "ID"), name=self.name,start=self.start_time, end=self.end_time, seconds=self.duration))

class SessionUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False,index=True, unique=True)
    token = db.Column(db.String(), nullable=False)
    proctor_id = db.Column(db.Integer, db.ForeignKey('proctor_session.id'))

    def generate_auth_token(self, duration):
        s = Serializer(app.config['SECRET_KEY'], expires_in = duration)
        self.token = s.dumps({'id':self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return "TOKEN_EXPIRE"
        except BadSignature:
            return "BAD_TOKEN"            
        user = SessionUser.query.get(data['id'])
        return user
    
    def __repr__(self):
        return (" -{id}-   {name}\n\t{email}\n\t{token}\n\t{proctor_id} ".format(id=self.id or "ID",name=self.name, email=self.email, token=self.token, proctor_id=self.proctor_id))

