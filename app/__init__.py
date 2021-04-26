from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_socketio import SocketIO
app = Flask(__name__)
app.hcount = 1
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'auth.login'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

from app import routes, models

from app.blueprint import auth
from app.blueprint import examinee
from app.blueprint import proctor

app.register_blueprint(auth.bp)
app.register_blueprint(examinee.bp)
app.register_blueprint(proctor.bp)