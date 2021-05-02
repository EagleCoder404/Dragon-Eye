from app.forms import ProctorSessionForm
from app import db
from app.models import ProctorSession, SessionUser
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime
bp = Blueprint("proctor", __name__, url_prefix="/proctor")

@bp.route("/", methods=["GET"])
@login_required
def index():
    ps = current_user.proctor_sessions
    return render_template("proctor_home.html",proctor_session_data=ps)


@bp.route("/session_create", methods=["GET", "POST"])
@login_required 
def session_create():
    form = ProctorSessionForm()
    if form.validate_on_submit():
        session_name = form.session_name.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        duration = (end_time - start_time).total_seconds()
        token_duration = (end_time - datetime.now()).total_seconds()
        
        #create a Proctor Session
        ps = ProctorSession(name=session_name, start_time=start_time, end_time=end_time, duration=duration, user_id=current_user)
        db.session.add(ps)
        
        susers = []
        #create session user for Proctor Session
        for suser in form.session_users:
             user = SessionUser(name=suser.username.data, email=suser.email.data, proctor_session=ps, token="token not set yet")
             db.session.add(user)
             susers.append(user)
        db.session.commit() #commit changes to db so that ids are assigned.

        for suser in susers:
            suser.generate_auth_token(token_duration)
            db.session.add(suser)
        db.session.commit()

        return redirect(url_for("proctor.index"))
    else:
        return render_template("proctorsessioncreator.html", form=form)

@bp.route("/session_details/<id>")
def session_details(id):
    ps = ProctorSession.query.get(id)
    if ps is None:
        return "Session not Found"
    else:
        return render_template("proctorsessiondetails.html", data = ps)