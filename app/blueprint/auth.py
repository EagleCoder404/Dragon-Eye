from flask import Blueprint, flash, redirect, url_for, render_template, flash, jsonify
from flask_login import login_user, logout_user
from app.models import User, SessionUser
from app import db, tokenAuth
from app.forms import LoginForm, RegistrationForm, TeacherRegistrationForm

bp = Blueprint("auth", __name__, url_prefix="/auth")



@bp.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('auth.login'))
        if user.user_type == "ATEACH":
                flash("Your account is not validated by the admin yet")
                return redirect(url_for('auth.login'))
        login_user(user)
        if user.user_type == "TEACH":
            return redirect(url_for('proctor.index'))
        if user.user_type == "ADMIN":
            return redirect(url_for('admin.index'))
    return render_template('login.html', form=form)


@bp.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        if User.query.filter_by(username=form.username.data).first() is not None:
            flash("Username already used")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=form.email.data).first() is not None:
            flash("Email already used")
            return redirect(url_for('auth.register'))

        user = User(username=form.username.data, email=form.email.data, user_type="ADMIN")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@bp.route("/new_teacher", methods=['GET', 'POST'])
def teacher_register():
    form = TeacherRegistrationForm()
    if form.validate_on_submit():

        if User.query.filter_by(username=form.username.data).first() is not None:
            flash("Username already used")
            return redirect(url_for('auth.teacher_register'))

        if User.query.filter_by(email=form.email.data).first() is not None:
            flash("Email already used")
            return redirect(url_for('auth.teacher_register'))
        admin = User.query.get(int(form.admin_code.data))
        user = User(username=form.username.data, email=form.email.data, user_type="ATEACH", admin_id=admin.id)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('teacher_registration.html', form=form) 

@bp.route("/token")
@tokenAuth.login_required
def token_login():
    user = tokenAuth.current_user()
    if user is None:
        return {'msg':'user not found'}
    else:
        ps = user.proctor_session
        data = { 'name':ps.name, 'id':ps.id,'start_time':ps.start_time,'end_time':ps.end_time,'duration':ps.duration, "submitted": user.submitted}
        return { 'msg':"GOOD_TOKEN", "data":data}


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
