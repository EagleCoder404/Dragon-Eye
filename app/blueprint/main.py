from flask import Blueprint, render_template, request
from app.models import Log
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

@bp.route("/logs")
def get_all_logs():
    logs = Log.query.all()
    log_csv = []
    headers = ["log_id"]+ list(logs[0].proctoring_logs[0].keys())
    for log in logs:
        for x in log.proctoring_logs:
            row = [log.id] + list(x.values())
            row = list(map(str, row))
            log_csv.append(row)
    print(log_csv[4:20])
    return render_template('logs.html',log_csv=log_csv, headers=headers)