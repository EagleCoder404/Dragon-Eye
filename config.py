import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") and os.environ.get("DATABASE_URL").replace("://", "ql://", 1)) or 'sqlite:///'+os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
