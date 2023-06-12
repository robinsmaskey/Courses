from uuid import UUID

from account.selectors import child_get_from_user
from course.models import Lesson
from course.selectors import (course_get_from_name, lesson_get_from_uid,
                              unit_get_from_uid)
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from progress.models import ChildSubunit

User = get_user_model()

# Tech debt: no need to return None. Raise validation error in the selector itself.


def course_progress_get(*, user: User, course_name: str) -> int:
    """
    Returns the course progress for a given user. Raises validation error if not found.
    """
    child = child_get_from_user(user=user)
    if child is None:
        raise ValidationError(_("User not associated with child."))

    course = course_get_from_name(course_name=course_name)
    if course is None:
        raise ValidationError(_("Invalid course name"))

    completed_subunit_count = ChildSubunit.objects.filter(
        child=child, subunit__course=course, completed=True
    ).count()
    total_subunits_in_course = course.subunit.count()

    progress_percentage = (completed_subunit_count / total_subunits_in_course) * 100

    return int(progress_percentage)


def lesson_progress_get(*, user: User, lesson_uid: str) -> int:
    """
    Returns the course progress for a given user. Raises validation error if not found.
    """
    child = child_get_from_user(user=user)
    if child is None:
        raise ValidationError(_("User not associated with child."))
    lesson = lesson_get_from_uid(uid=lesson_uid)
    if lesson is None:
        raise ValidationError(_("User not associated with child."))

    completed_subunit_count = ChildSubunit.objects.filter(
        child=child, subunit__lesson=lesson, completed=True
    ).count()
    total_subunits_in_lesson = lesson.subunit.count()

    progress_percentage = (completed_subunit_count / total_subunits_in_lesson) * 100

    return int(progress_percentage)


def unit_progress_get(*, user: User, unit_uid: UUID) -> int:
    """
    Returns the course progress for a given user. Raises validation error if not found.
    """
    child = child_get_from_user(user=user)
    if child is None:
        raise ValidationError(_("User not associated with child."))
    unit = unit_get_from_uid(unit_uid=unit_uid)
    if unit is None:
        raise ValidationError(_("User not associated with child."))

    completed_subunit_count = ChildSubunit.objects.filter(
        child=child, subunit__unit=unit, completed=True
    ).count()
    total_subunits_in_unit = unit.subunit.count()

    progress_percentage = (completed_subunit_count / total_subunits_in_unit) * 100

    return int(progress_percentage)
