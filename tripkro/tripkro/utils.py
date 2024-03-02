import jwt

from jwt.exceptions import InvalidTokenError

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rest_framework import serializers

from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse


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


# respose error structure
class CustomExceptionFormatter(ExceptionFormatter):
    def format_error_response(self, error_response: ErrorResponse):
        error_messages = []
        for error in error_response.errors:
            if (
                error_response.type == "validation_error"
                and error.attr
                and error.attr != "non_field_errors"
            ):
                error_message = f"{error.attr}: {error.detail}"
            else:
                error_message = error.detail
            error_messages.append(error_message)
        formatted_response = {"status": 400, "error": error_messages}
        return formatted_response


# custom error serializer
class CustomErrorSerializer(serializers.Serializer):
    def to_representation(self, instance):
        error_list = []
        for field, errors in instance.items():
            for error in errors:
                error_message = f"{field}: {error}"
                error_list.append(error_message)
        return error_list
