import os

from django.conf import settings
from django.utils import timezone

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from rest_framework_simplejwt.tokens import RefreshToken

from tripkro.utils import send_html_email, encode_token


def send_email_verify_mail(email):

    payload = {"email": email, "exp": timezone.now() + timezone.timedelta(days=1)}
    token = encode_token(payload)
    template = "emails/sign_up_email_verify.html"
    redirect_url = f"{settings.FRONT_END_URL}/api/account/verify-email/{token}/"

    send_html_email(
        email, "Verify your email", template, context={"redirect_url": redirect_url}
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)


def twilio_send_otp(phone):
    try:
        verify.verifications.create(to=phone, channel="sms")
    except Exception as e:
        return e.args


def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
        return result.status == "approved"
    except TwilioRestException as e:
        return e.args
