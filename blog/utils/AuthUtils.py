from flask_mail import Message
from blog import conf, mail
from flask import url_for

def send_reset_pwd_email(user):
    token = user.get_reset_pwd_token()
    msg = Message("Password Reset Request", sender=conf.MAIL_USERNAME, recipients=[user.email])
    msg.body = f"""{ url_for('AuthRoute.reset_password', token=token, _external=True) }
to reset the password click on the following link:"""
    mail.send(msg)



