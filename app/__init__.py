from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import BaseConfiguration, TestConfiguration
from flask_login import LoginManager
from flask_moment import Moment
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
tokenAuth = HTTPTokenAuth()
login = LoginManager()
cors = CORS()
mail = Mail()
login.login_view = 'auth.login'



def create_app(config_class=BaseConfiguration):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app,db)
    moment.init_app(app)
    login.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    
    from app.blueprint import auth
    app.register_blueprint(auth.bp)

    from app.blueprint import examinee
    app.register_blueprint(examinee.bp)

    from app.blueprint import proctor
    app.register_blueprint(proctor.bp)

    from app.blueprint import admin
    app.register_blueprint(admin.bp)

    from app.blueprint import main
    app.register_blueprint(main.bp)

    return app

from app import models

