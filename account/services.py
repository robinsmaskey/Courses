import numbers
from dataclasses import dataclass

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .helpers import generate_six_digit_otp, send_otp
from .models import Child, Guardian, Otp, PortalUser
from .selectors import (child_get_from_user, guardian_email_get_from_user,
                        guardian_get, guardian_get_all_children,
                        otp_get_from_user, otp_get_from_user_and_number,
                        user_get, user_get_from_guardian_email)

User = get_user_model()

# Tech debt: You can get user from request.user, no need to send email manually.


@transaction.atomic
def user_signup(
    *,
    full_name: str,
    username: str,
    password: str,
    confirm_password: str,
    user_type: str,
) -> PortalUser:

    """
    Signs up the user and returns a user object.
    """
    map_user_type_to_user_verification = {"child": True, "guardian": False}
    user_is_verified = map_user_type_to_user_verification[user_type]

    if password != confirm_password:
        raise ValidationError(_("Password & confirm password fields do not match."))

    existing_user = user_get(username=username)
    if existing_user is not None:
        raise ValidationError(_("User with that username already exists."))

    try:
        validate_password(password)
    except DjangoValidationError as e:
        raise ValidationError(_(str(e.messages[0])))

    user = User(
        full_name=full_name,
        username=username,
        user_type=user_type,
        is_verified=user_is_verified,
    )
    user.set_password(password)

    try:
        print("Attempting to clean the user.")
        user.full_clean()
    except Exception as e:
        raise ValidationError(_(str(e)))
    print("Attempting to save the user.")
    user.save()
    return user


@transaction.atomic
def guardian_signup(
    *, full_name: str, username: str, email: str, password: str, confirm_password: str
) -> object:
    """
    Signs up and returns a GuardianSignupDetails dataclass object.
    Sends OTP after the signup is complete.
    """

    @dataclass(frozen=True)
    class GuardianSignupDetails:
        user_type: str
        username: str
        full_name: str
        email: str
        is_verified: bool
        access_token: str

    user_type = "guardian"
    try:
        user = user_signup(
            full_name=full_name,
            username=username,
            password=password,
            confirm_password=confirm_password,
            user_type=user_type,
        )
    except Exception as e:
        print("This is what happened")
        raise ValidationError(_(str(e)))
    try:
        guardian = Guardian(user=user, email=email)
        guardian.full_clean()
    except DjangoValidationError as e:
        raise ValidationError(_(str(e.messages[0])))

    guardian.save()

    token = RefreshToken.for_user(user)
    refresh_token = str(token)
    access_token = str(token.access_token)

    is_verified = user.is_verified
    user_type = user_type

    signup_details = GuardianSignupDetails(
        user_type, username, full_name, email, is_verified, access_token
    )

    return signup_details, refresh_token


def guardian_login(*, username: str, password: str) -> tuple:
    """
    Verifies guardian user's credentials & returns access token & refresh token.
    """

    @dataclass(frozen=True)
    class GuardianLoginDetails:
        user_type: str
        username: str
        full_name: str
        is_verified: bool
        access_token: str

    user = user_get(username=username)

    if user is None:
        raise ValidationError(_("User does not exist."))

    if user.user_type == "child":
        raise ValidationError(_("Invalid user type. Not a guardian."))

    if not user.check_password(password):
        raise ValidationError(_("Invalid password"))

    user_type = user.user_type
    full_name = user.full_name
    is_verified = user.is_verified

    token = RefreshToken.for_user(user)
    access_token = str(token.access_token)
    refresh_token = str(token)

    guardian_login_details = GuardianLoginDetails(
        user_type, username, full_name, is_verified, access_token
    )

    return guardian_login_details, refresh_token


@transaction.atomic
def child_signup(
    *, guardian_email: str, full_name: str, username: str, pin: int, confirm_pin: int
) -> object:
    """
    Verifies a chid's user credentials & returns access and refresh tokens.
    """

    @dataclass
    class ChildSignupDetails:
        user_type: str
        username: str
        full_name: str
        is_verified: bool
        access_token: str

    user = user_signup(
        full_name=full_name,
        username=username,
        password=pin,
        confirm_password=confirm_pin,
        user_type="child",
    )
    child = Child(user=user)
    child.full_clean()
    child.save()

    guardian = guardian_get(email=guardian_email)
    if guardian is None:
        raise ValidationError(_("Guardian does not exist."))

    guardian.children.add(child)
    guardian.save()

    token = RefreshToken.for_user(user)
    access_token = str(token.access_token)
    refresh_token = str(token)
    is_verified = user.is_verified
    user_type = user.user_type

    child_signup_details = ChildSignupDetails(
        username, full_name, is_verified, access_token, user_type
    )

    return child_signup_details, refresh_token


def child_login(*, email: str, username: str, pin: str) -> tuple:
    """
    Returns an access token, a refresh token, and the username of the child.
    """
    @dataclass(frozen=True)
    class ChildLoginDetails:
        user_type: str
        username: str
        full_name: str
        is_verified: bool
        access_token: str

    user = user_get(username=username)
    if user is None:
        raise ValidationError(_("User does not exist."))

    password_is_valid = user.check_password(pin)

    if not password_is_valid:
        raise ValidationError(_("Password invalid"))

    guardian = guardian_get(email=email)
    if guardian is None:
        raise ValidationError(_("Guardian does not exist."))

    child = child_get_from_user(user=user)
    if child is None:
        raise ValidationError(_("Child does not exist"))

    if child not in guardian_get_all_children(guardian=guardian):
        raise ValidationError(_("Guardian not associated with child."))

    token = RefreshToken.for_user(user)

    refresh_token = str(token)
    access_token = str(token.access_token)

    username = username
    user_type = user.user_type
    full_name = user.full_name
    is_verified = user.is_verified


    child_login_details = ChildLoginDetails(username, 
    user_type, full_name, is_verified, access_token)

    return child_login_details, refresh_token


@transaction.atomic
def guardian_verify(*, user: PortalUser, otp: int) -> PortalUser:
    """
    Verifies the user if a given otp is valid.
    """
    otp_object = otp_get_from_user_and_number(user=user, otp_number=otp)
    if otp_object.has_expired or otp_object is None:
        raise ValidationError(_("Otp invalid. Please request a new one."))
    user.is_verified = True
    user.full_clean()
    user.save(update_fields=["is_verified"])

    otp_object.delete()

    return user


@transaction.atomic
def otp_send(*, guardian_email: str) -> Otp:
    """
    Sends an otp to a given email.
    """
    user = user_get_from_guardian_email(email=guardian_email)
    if user is None:
        raise ValidationError(_("User with the given email does not exist."))
    otp_number = generate_six_digit_otp()

    otp = Otp(otp=otp_number, user=user)
    otp.full_clean()
    otp.save()

    send_otp(otp_number=otp_number, receiver_email=guardian_email)

    return otp


@transaction.atomic
def otp_resend(*, user: PortalUser) -> Otp:
    """
    Resends an otp to a given email. Returns 401 if an otp object does not already exist.
    """
    otp = otp_get_from_user(user=user)
    if otp is not None:
        otp.delete()

    if user.is_verified:
        raise ValidationError(_("User already verified."))

    otp_number = generate_six_digit_otp()
    otp = Otp(otp=otp_number, user=user)
    otp.full_clean()
    otp.save()

    guardian_email = guardian_email_get_from_user(user=user)
    otp = send_otp(otp=otp, guardian_email=guardian_email)
    return otp
