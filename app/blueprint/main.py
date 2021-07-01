from flask import Blueprint, render_template, request

bp = Blueprint("main",__name__,url_prefix="/")


@bp.route("/")
@bp.route("/index")
def index():
    # test = socketio.async_mode
    return render_template('index.html')

@bp.route("/test", methods=['GET', 'POST'])
def excel_test():
    print()
    print(request.form.get("lol"))
    print()
    return render_template("test.html")