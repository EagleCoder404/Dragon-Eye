from flask.helpers import make_response
from sqlalchemy.orm import eagerload
from app.forms import ProctorSessionForm, ExamFormForm
from app import db
from app.models import User
from flask import Blueprint, render_template, redirect, url_for, json
from flask_login import login_required, current_user

from app.blueprint.helper.email_helpers import mail_all

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/")
@login_required
def index():
    teachers = User.query.filter_by(admin_id=current_user.id)
    return render_template("admin_home.html", teachers=teachers, admin_code=current_user.id)

@bp.route("/delete/<id>", methods=['GET', 'POST'])
@login_required
def delete_teacher(id):
    teacher = User.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for("admin.index"))

@bp.route("/accept/<id>", methods=['GET', 'POST'])
@login_required
def accept_teacher(id):
    teacher = User.query.get_or_404(id)
    teacher.user_type="TEACH"
    db.session.commit()
    return redirect(url_for("admin.index"))