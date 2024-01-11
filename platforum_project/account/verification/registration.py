from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import CustomUser
from account.verification import email_verification_token


def send_email_verification(request, user: CustomUser):
    current_site = get_current_site(request)
    subject = 'Activation du compte PlatForum'
    body = render_to_string(
        'email/verification.html',
        {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_verification_token.make_token(user),
        }
    )
    EmailMessage(to=[user.email], subject=subject, body=body).send()
