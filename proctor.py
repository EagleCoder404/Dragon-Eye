from app import app, db, socketio
from app.models import User

# socketio.run(app)
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', debug=True)

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'si':socketio}