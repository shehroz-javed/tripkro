from django.conf import settings
from django.utils import timezone

from tripkro.utils import send_html_email, encode_token


def send_email_verify_mail(email):

    payload = {"email": email, "exp": timezone.now() + timezone.timedelta(days=1)}
    token = encode_token(payload)
    template = "emails/sign_up_email_verify.html"
    redirect_url = f"{settings.FRONT_END_URL}/api/account/verify-email/{token}/"

    send_html_email(
        email, "Verify your email", template, context={"redirect_url": redirect_url}
    )
