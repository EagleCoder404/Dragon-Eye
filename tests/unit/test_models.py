from sqlalchemy.orm import selectin_polymorphic
from app.models import User, ProctorSession, SessionUser
from app import db, create_app
from sqlalchemy import exc
from pytz import timezone
from time import sleep

def toUtc(d):
    utc = timezone("utc")
    return utc.localize(d)
    
def test_new_user(app):
    user = User(username='harsha', email="harsha.jediknight@gmail.com")
    user.set_password("harsha")
    db.session.add(user)
    db.session.commit()

    assert user != None
    assert user.check_password("harsha") == True
    assert user.check_password("hello") == False

def test_duplicate_user(app):
    try:
        user1 = User(username='harsha', email="harsha.jediknight@gmail.com")
        user2 = User(username='harsha', email="harsha.jediknight@gmail.com")
        db.session.add(user2)
        db.session.add(user1)
        db.session.commit()

        assert False
    except exc.IntegrityError:
        assert True

def test_proctor_session(app, new_user, start_time, end_time):
    duration = (end_time - start_time).total_seconds()
    proctor_session = ProctorSession(name='test', start_time=start_time, end_time=end_time, duration=duration, user_id=new_user)
    db.session.add(new_user)
    db.session.add(proctor_session)
    db.session.commit()


    assert proctor_session.name == 'test'    
    assert toUtc(proctor_session.start_time) == start_time
    assert toUtc(proctor_session.end_time) == end_time

def test_session_user(app, new_session_user):
    new_session_user.generate_auth_token(1)
    token = new_session_user.token

    db.session.add(new_session_user)
    db.session.commit()
    
    assert token != None
    assert SessionUser.verify_auth_token(token).id == new_session_user.id

    sleep(2) # wait for the token to expire

    assert SessionUser.verify_auth_token(token) == "TOKEN_EXPIRE"