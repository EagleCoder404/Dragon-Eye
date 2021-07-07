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

@bp.route("/cum")
def cumulative():

    logs = Log.query.all()
    log_csv = []
    headers = ["log_id"]+ list(logs[0].proctoring_logs[0].keys())
    headers.remove("frame_id")
    for log in logs:
        face_not_detected = 0
        face_not_recognized = 0
        face_multi = 0 
        face_sideways = 0
        eye_sideways = 0
        for x in log.proctoring_logs:
            if(x['face_detection'] == "False"):
                face_not_detected += 1
            if(x['face_recognition'] == "False"):
                face_not_recognized += 1           
            if(x['multiple_face'] == "True"):
                face_mult += 1
            if(x["face_alignment"] == "left" or x['face_alignment'] == "right"):
                face_sideways += 1
            if(x['eye_position'] == "left" or x['eye_position'] == "right"):
                eye_sideways += 1
        row = [log.id, face_not_detected, face_multi, face_not_recognized, face_sideways, eye_sideways]
        row = list(map(str, row))
        log_csv.append(row)
    return render_template('logs.html', log_csv=log_csv, headers=headers)

