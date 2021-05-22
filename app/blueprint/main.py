from flask import Blueprint, render_template

bp = Blueprint("main",__name__,url_prefix="/")


@bp.route("/")
@bp.route("/index")
def index():
    # test = socketio.async_mode
    return render_template('index.html')

@bp.route("/excel_test")
def excel_test():
    return render_template("test_excel_parser.html")