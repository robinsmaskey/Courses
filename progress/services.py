from course.models import Subunit
from course.selectors import subunit_get_from_uid
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .models import ChildSubunit

User = get_user_model()


def subunit_progress_create(*, user: User, subunit_uid: str) -> ChildSubunit:
    """
    Function used to add / create a child's progress throughout the course.
    Returns ChildCourse object if created successfully.
    """
    child = user.child.first()
    if child is None:
        raise ValidationError(_("Invalid user type. User should be of child type."))
    subunit = subunit_get_from_uid(uid=subunit_uid)
    if subunit is None:
        raise ValidationError(_("Subunit does not exist."))

    try:
        child_subunit = ChildSubunit.objects.get(
            subunit=subunit, child=child, completed=True
        )
    except ChildSubunit.DoesNotExist:
        subunit_progress = ChildSubunit(subunit=subunit, child=child, completed=True)
        subunit_progress.full_clean()
        subunit_progress.save()

        return True
    return False
