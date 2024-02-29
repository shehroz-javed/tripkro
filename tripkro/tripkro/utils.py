import jwt

from jwt.exceptions import InvalidTokenError

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rest_framework import serializers
from rest_framework.views import exception_handler


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


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, serializers.ValidationError):
            errors = response.data
            field_errors = {}

            for field, error_detail in errors.items():
                field_name = field.split("_")[0] if "_" in field else field
                field_errors[field_name] = error_detail

            response.data = {"errors": field_errors}

    return response
