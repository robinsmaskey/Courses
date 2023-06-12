from uuid import UUID

from account.models import PortalUser
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import (Case, FilteredRelation, OuterRef, QuerySet,
                              Value, When)
from django.db.models.functions import JSONObject
from progress.models import ChildCoursePreview
from rest_framework.exceptions import ValidationError

from .models import Course, CoursePreview, CourseReview, Lesson, Subunit, Unit

# Refactor this code / Very huge tech debt.
# Refactor names and variable names.


def course_preview_get_all(
    * course_name: str, **kwargs
) -> QuerySet[CoursePreview]:
    """
    Returns all the course preview objects associated with a given course.
    """
    user = kwargs.get("user")
    course_preview_set = None

    if user.is_anonymous:
        course_preview_set = CoursePreview.objects.filter(course__name=course_name)
        return course_preview_set
    else:
        course_preview_set = CoursePreview.objects.filter(
                course__name=course_name
            ).values('uid', 'name', 'link', 'type').annotate(progress=FilteredRelation('child_progress')).values(
                'uid', 'name', 'link', 'type',
                completed=Case(
                    When(child_progress__child__user=user, child_progress__completed=True, then=Value("True")),
                    default=Value("False")
                )
            )
    return course_preview_set



def course_review_get_all(
    *, course_name: str, **kwargs
) -> QuerySet[CourseReview]:
    """
    Returns all the course preview objects associated with a given course.
    """
    user = kwargs.get("user")
    course_review_set = None

    if user.is_anonymous:
        course_review_set = CourseReview.objects.filter(course__name=course_name)
        return course_review_set    
    else:
        course_review_set = CourseReview.objects.filter(
            course__name=course_name
        ).values("uid", "name", "type", "link", "text", "completion_score").annotate(
            progress=FilteredRelation('child_progress')
        ).values(
            "uid", "name", "link", "type", "text", "completion_score", completed=Case(
                When(child_progress__child__user=user, child_progress__completed=True, then=Value("True")), default=Value("False")
            )
        )
        return course_review_set    


def subunit_get_from_uid(*, uid: UUID) -> Subunit:
    """
    Selector function used to get subunit objects associated with a given uid.
    """
    try:
        subunit = Subunit.objects.get(uid=uid)
    except Subunit.DoesNotExist:
        return None
    return subunit


def course_get_from_name(*, course_name: str) -> Course:
    """
    Selector function that returns a course object from a given name.
    """
    try:
        course = Course.objects.get(name=course_name)
    except Course.DoesNotExist:
        return None
    return course


def lesson_get_from_uid(*, uid: UUID) -> Lesson:
    """
    Selector function that returns a lesson object from a given UID.
    """
    try:
        lesson = Lesson.objects.get(uid=uid)
    except Lesson.DoesNotExist:
        return None
    return lesson


def unit_get_from_uid(*, unit_uid: UUID) -> Unit:
    """
    Selector function that returns a unit object from a given UID.
    """
    try:
        unit = Unit.objects.get(uid=unit_uid)
    except Lesson.DoesNotExist:
        return None
    return unit


def get_all_courses() -> QuerySet[Course]:
    """
    Returns all the courses in the database
    """
    course = Course.objects.all()
    return course


def get_all_lessons_from_course(*, course_name: str) -> QuerySet[Lesson]:
    """
    Returns all the lessons associated with a given course
    """
    lessons = Lesson.objects.filter(course__name=course_name)
    return lessons


def get_all_units_from_lesson(*, lesson_uid: UUID, **kwargs) -> QuerySet:
    """
    Returns all the units associated with a given lesson uid.
    """
    user = kwargs.get('user')

    if user.is_anonymous:
        units = Unit.objects.filter(lesson__uid=lesson_uid)
        return units
    try:
        subunit_subquery = (
            Subunit.objects.filter(unit=OuterRef("pk"))
            .annotate(ChildSubunit=FilteredRelation("child_progress"))
            .values(
                json=JSONObject(
                    uid="uid",
                    name="name",
                    type="type",
                    completed=Case(
                        When(child_progress__child__user=user, then=Value("True")),
                        default=Value("False"),
                    ),
                )
            )
        )
    except ValueError:
        return None
    unit_queryset = (
        Unit.objects.filter(lesson__uid=lesson_uid)
        .annotate(subunits=ArraySubquery(subunit_subquery))
        .values()
    )
    if not unit_queryset.exists():
        return None
    return unit_queryset


def get_all_subunits_from_unit(*, unit_uid: str) -> QuerySet[Lesson]:
    """
    Returns all the subunits associated with a given unit
    """
    subunits = Subunit.objects.filter(unit__uid=unit_uid)
    return subunits


def get_subunit_from_uid(*, uid: str) -> Subunit:
    try:
        subunit = Subunit.objects.get(uid=uid)
    except Subunit.DoesNotExist:
        return None
    return subunit


# Send three values anyway
def get_adjacent_subunits_from_uid(*, uid: str) -> QuerySet[Subunit]:
    """
    Returns a queryset with Subunits having adjacent ids.
    For example:
    For a subunit of id 2, it returns a queryset of subunit with id 1, 2, & 3.
    """
    try:
        subunit = Subunit.objects.get(uid=uid)
    except Subunit.DoesNotExist:
        return None
    qset = Subunit.objects.filter(id__range=(subunit.id - 1, subunit.id + 1))
    return qset


def next_subunit_get(*, current_subunit_uid: str) -> Subunit:
    """
    Returns a subunit object adjacent to a given subunit uid.
    For example:
    For a subunit with id 1, this function will return subunit with and id of 2.
    """
    try:
        current_subunit = Subunit.objects.get(uid=current_subunit_uid)
    except Subunit.DoesNotExist:
        return None
    try:
        next_subunit = Subunit.objects.get(id=current_subunit.id + 1)
    except Subunit.DoesNotExist:
        return None
    return next_subunit


def previous_subunit_get(*, current_subunit_uid: str) -> Subunit:
    """
    Returns a subunit object adjacent to a given subunit uid.
    For example:
    For a subunit with id 1, this function will return subunit with and id of 2.
    """
    try:
        current_subunit = Subunit.objects.get(uid=current_subunit_uid)
    except Subunit.DoesNotExist:
        return None
    try:
        next_subunit = Subunit.objects.get(id=current_subunit.id - 1)
    except Subunit.DoesNotExist:
        return None
    return next_subunit
