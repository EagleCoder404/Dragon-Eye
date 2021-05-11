from flask import Blueprint
from flask.helpers import make_response
from app import tokenAuth, db

bp = Blueprint("examinee",__name__,url_prefix="/session")

@bp.route("/",methods=['GET'])
def index():
    return "User Session"

@bp.route("/test")
@tokenAuth.login_required
def test():
    print(tokenAuth.current_user())
    return "It Works"

@bp.route("/id_card/<link>")
@tokenAuth.login_required
def add_id_card(link):
    session_user = tokenAuth.current_user()
    session_user.id_card = link
    db.session.commit()
    return make_response({"msg":"added id card link", link:link},200)
