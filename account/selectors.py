from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from .models import Child, Guardian, Otp, PortalUser

User = get_user_model()


def user_get(*, username: str) -> User:
    """
    Returns a user model object that matches the given username. Returns none if the user object does not exist.
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    return user


def guardian_get(*, email: str) -> Guardian:
    """
    Returns a guardian model object that matches the given email.
    Returns none if the guardian object does not exist.
    """
    try:
        guardian = Guardian.objects.get(email=email)
    except Guardian.DoesNotExist:
        return None

    return guardian


def user_get_from_guardian_email(*, email: str) -> PortalUser:
    """
    Returns the user object a guardian is associated with from an email.
    Returns None if the user does not exist.
    """
    try:
        user = User.objects.get(guardian__email=email)
    except PortalUser.DoesNotExist:
        return None
    return user


def guardian_child_list(*, email: str) -> QuerySet:
    """
    Returns a list of child for a given guardian email.
    """
    try:
        guardian = Guardian.objects.get(email=email).prefetch_related("children")
    except Guardian.DoesNotExist:
        raise ObjectDoesNotExist(_("Guardian does not exist."))

    queryset = (
        guardian.children.prefetch_related("user")
        .annotate(
            full_name=F("user__full_name"),
            address=F("user__address"),
            username=F("user__username"),
        )
        .values("full_name", "address", "username")
    )

    return queryset


def guardian_get_all_children(*, guardian: Guardian) -> QuerySet[Child]:
    """
    Used only for validation/internal purposes.
    Returns a list of all children associated with a given guardian object.
    Returns none if no children are available.
    """
    children = guardian.children.all()
    if children is None:
        return None
    return children


def child_get_from_user(*, user: PortalUser) -> Child:
    """
    Returns the child object associated with the user.
    Returns none if not found.
    """
    child = user.child.first()
    if child is None:
        return None
    return child


# def user_get_from_access_token(*, access_token: str) -> PortalUser:
#     """
#     Returns the user who is associated with a given access token.
#     """
#     token = AccessToken(str(access_token))
#     user_id = token.get("user_id")
#     if user_id is not None:
#         try:
#             user = PortalUser.objects.get(pk=user_id)
#         except PortalUser.DoesNotExist:
#             raise ValidationError(_("Invalid user."))
#         return user
#     raise ValidationError(_("Invalid access token"))


def otp_get_from_user_and_number(*, user: str, otp_number: int) -> QuerySet[Otp]:
    """
    Returns an otp object from a given otp number. Returns None if not found.
    """
    otp = Otp.objects.filter(otp=otp_number, user=user).first()
    if otp is not None:
        return otp
    return None


def otp_get_from_user(*, user: PortalUser) -> Otp:
    """
    Returns an otp object from an user object.
    """
    try:
        otp = Otp.objects.get(user=user)
    except Otp.DoesNotExist:
        return None
    return otp


def guardian_email_get_from_user(*, user: PortalUser) -> str:
    """
    Returns the guardian object associated with a user object.
    Returns none if not found.
    """
    try:
        email = user.guardian.first().email
    except Guardian.DoesNotExist:
        return None
    return email


def child_get(username):
    try:
        child = Child.objects.get(user__username=username)
    except Child.DoesNotExist:
        return None
    return child
