from attr import dataclass
import pytest
from app import create_app, db
from app.models import User
from pytz import timezone
from datetime import datetime
class TestConfiguration(object):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'

@pytest.fixture(scope='function')
def app():
    app = create_app(TestConfiguration)
    app_context = app.app_context()
    app_context.push()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def new_user():
    user = User(username='harsha', email='harsha.jediknigtht@gmail.com')
    user.set_password("harsha")

    return user


@pytest.fixture(scope='function')
def start_time():
    utc = timezone('utc')
    now = utc.localize(datetime.utcnow())
    return now

@pytest.fixture(scope='function')
def end_time(start_time):
    utc = timezone('utc')
    now = datetime.fromtimestamp(start_time.timestamp()+2)

    return utc.localize(now)

