from flask import Blueprint
from flask_login import login_required, current_user
bp = Blueprint("examinee",__name__,url_prefix="/session")

@bp.route("/",methods=['GET'])
@login_required
def index():
    return "User Session"

