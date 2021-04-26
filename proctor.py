from app import app, db, socketio
from app.models import User, ProctorSession, SessionUser

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'PS':ProctorSession, "SU":SessionUser}