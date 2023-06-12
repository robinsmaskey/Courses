import math
import random

from django.conf import settings
from django.core.mail import send_mail


def generate_six_digit_otp() -> int:
    """
    Generates a six digit otp number.
    """
    otp = random.randint(100000, 999999)
    return otp


def send_otp(*, otp_number: int, receiver_email: str) -> bool:
    """
    Sends otp to a given email and returns True if executed.
    """
    subject = "Account verification email"
    message = f"Your otp is {otp_number}"
    email_from = settings.EMAIL_HOST
    email_to = receiver_email

    send_mail(subject, message, email_from, [email_to], fail_silently=False)

    return True
