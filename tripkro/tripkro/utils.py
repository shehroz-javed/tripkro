import jwt

from jwt.exceptions import InvalidTokenError

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


# to send the email
def send_html_email(email_to=None, subject="", template="", context={}):

    html_message = render_to_string(template_name=template, context=context)
    from_email = settings.EMAIL_HOST_USER
    email = EmailMessage(
        subject=subject, body=html_message, from_email=from_email, to=[email_to]
    )
    email.content_subtype = "html"
    email.send()


# to encode the token
def encode_token(pyload):

    secret_key = settings.SECRET_KEY
    token = jwt.encode(pyload, secret_key, algorithm="HS256")
    return token


# decode the token
def decode_token(token):
    try:
        secret_key = settings.SECRET_KEY
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except Exception as e:
        raise InvalidTokenError(f"Invalid token : {e}")
