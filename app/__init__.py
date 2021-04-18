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
login.login_view = 'login'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

from app import routes, models
