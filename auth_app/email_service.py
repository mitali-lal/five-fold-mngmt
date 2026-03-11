from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_verification_email(user, token):
    verification_url = f"{settings.SITE_URL}/verify-email/{token}/"

    html_message = render_to_string(
        'auth_app/verification_email.html',
        {
            'user': user,
            'verification_url': verification_url
        }
    )

    plain_message = strip_tags(html_message)

    send_mail(
        subject='Verify your FFMS account',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False
    )
