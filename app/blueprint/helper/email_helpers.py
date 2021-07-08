from app import mail
from flask_mail import Message
from string import Template

def generateMessageBody(details):
    return Template(""" 
    Hey There !.
    You have $test_name soon,
    it starts at $start_time, and ends at $end_time,
    That's $duration minutes, 

    Use the Token below to login succesfully into our app.
    $token
    """).substitute(
        test_name=details['test_name'],
        start_time=details['start_time'],
        end_time=details['end_time'],
        duration=details['duration'],
        token=details['token'])

def send_email(subject, sender, recipients, text_body, html_body=""):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def mail_all(proctor_session,session_users):
    details = {}
    details['test_name'] = proctor_session.name
    details['start_time'] = proctor_session.start_time
    details['end_time'] = proctor_session.end_time
    details['duration'] = proctor_session.duration

    for session_user in session_users:
        session_user_details = dict(details)
        session_user_details['token'] = session_user.token
        print(session_user_details)
        message_text_body = generateMessageBody(session_user_details)
        send_email(
            subject="Test Details", 
            sender="dragon.eye.finalyear@gmail.com", 
            recipients=[session_user.email], 
            text_body=message_text_body )
