from flask.helpers import url_for
from flask_login.utils import login_required, logout_user
from app import app, socketio
from flask_login import current_user, login_user
from app.models import User
from app.forms import LoginForm
from flask import redirect, render_template, flash, request
# from flask_socketio import emit
@app.route("/")
@app.route("/index")
@login_required
def index():
    user = {'username':'Harsha'}
    test = socketio.async_mode
    return render_template('index.html',title='Proctor',user=user,test=test)

@app.route('/login',methods=['GET','POST'])
def login():
    print('lol')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/client')
def client():
    return render_template('client.html')

@socketio.on('image')
def image(data):
    socketio.emit('response_back',data)