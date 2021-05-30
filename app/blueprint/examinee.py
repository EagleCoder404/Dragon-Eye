from flask import Blueprint, json
from flask.globals import request
from flask.helpers import make_response
from flask_migrate import current
from app import tokenAuth, db
from app.models import ExamResponse
from sqlalchemy.orm.attributes import flag_modified

bp = Blueprint("examinee",__name__,url_prefix="/session")

@bp.route("/",methods=['GET'])
def index():
    return "User Session"

@bp.route("/test")
@tokenAuth.login_required
def test():
    print(tokenAuth.current_user())
    return "It Works"

@bp.route("/id_card/", methods=["POST"])
@tokenAuth.login_required
def add_id_card():
    data = request.get_json()
    link = data['link']
    session_user = tokenAuth.current_user()
    session_user.id_card = link
    db.session.commit()
    return make_response({"msg":"added id card link", link:link},200)

@bp.route("/exam/answer/get/<question_id>")
@bp.route("/exam/answer/get")
@tokenAuth.login_required
def get_question_answer(question_id=None):
    exam_response = tokenAuth.current_user().exam_response
    if exam_response == None:
        return make_response({"msg":"no response submitted"}, 404)
    exam_response = json.loads(exam_response.response)
    answer_data = exam_response.answer_data
    if question_id is not None:
        if question_id in answer_data.keys():
            return make_response({"data":answer_data[question_id]}, 200)
        else:
            return make_response({"msg":"invalid question id"}, 404)
    else:
        return make_response({"data":answer_data})

@bp.route("/exam/update", methods=["POST"])
@tokenAuth.login_required
def update_answer():
    current_user = tokenAuth.current_user()
    exam_response = current_user.exam_response
    exam_form = list(current_user.proctor_session.exam_form)
    updated_answers_data = request.get_json()

    if exam_form != []:    
        exam_form = exam_form[0]
        if exam_response is None:
            form_description = exam_form.form_description
            response = { 'answer_data':[] }
            for id in range(len(form_description['exam_questions'])):
                answer = { "id":id, "answer": ""}
                response['answer_data'].append(answer)
            exam_response = ExamResponse(response=response, session_user_id=current_user, exam_form=exam_form)
            db.session.add(exam_response)
            db.session.commit()

        if updated_answers_data['data'] != []:
            response = exam_response.response
            max_id = len(response['answer_data'])
            for answer in updated_answers_data['data']:
                if( int(answer['id']) > max_id):
                    return make_response({'msg':"invald question id"}, 500)
                current_answer_data = response['answer_data'][int(answer['id'])]
                current_answer_data['answer'] = answer['answer']
            exam_response.response = response
            flag_modified(exam_response,'response')
            db.session.add(exam_response)
            db.session.commit()

            return make_response({"msg":"Done"}, 200)
        else:
            return make_response({"msg":"Empty Data Recived"}, 400)
    else:
        return make_response({"msg":"exam form has not be assigned to the test yer"}, 204)

@bp.route("/exam/question/get")
@tokenAuth.login_required
def get_question():
    exam_form = list(tokenAuth.current_user().proctor_session.exam_form)
    exam_response = tokenAuth.current_user().exam_response
    if exam_form == []:
        return make_response({"msg":"exam form hasn't been added yet"}, 204)
    else:
        exam_form = exam_form[0]
        form_description = exam_form.form_description
        if exam_response is not None:
            form_description['answer_data'] = exam_response.response['answer_data']
        return make_response({'data':form_description}, 200)

@bp.route("/exam/submit")
@tokenAuth.login_required
def exam_submit():
    tokenAuth.current_user().submitted = True
    db.session.commit()
    return make_response({'msg':'done'}, 200)    