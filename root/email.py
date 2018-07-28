from flask import render_template
from flask_mail import Message
from root import mail, app
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_reset_email(user):
    token = user.get_reset_token()
    send_email('[Portfolio] Reset Your Password !important',
               sender='flasktestingemail@gmail.com',
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_contact_us_email(user, subject, body):
    send_email(subject,
               sender='flasktestingemail@gmial.com',
               recipients=[app.config['ADMIN']],
               text_body=render_template('email/contact_us.txt', user=user, body=body, subject=subject),
               html_body=render_template('email/contact_us.html', user=user, body=body, subject=subject)
               )