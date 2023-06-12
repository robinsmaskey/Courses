from account.models import Child
from config.model_mixins import IdentifierTimeStampAbstractModel
from course.models import (Course, CoursePreview, CourseReview, Lesson,
                           Subunit, Unit)
from django.db import models


class ChildCourse(IdentifierTimeStampAbstractModel):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="child_progress"
    )
    child = models.ForeignKey(
        Child, on_delete=models.PROTECT, related_name="course_progress"
    )
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.child} - {self.course}"

    class Meta:
        ordering = ["-created_date"]


class ChildLesson(IdentifierTimeStampAbstractModel):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="child_progress"
    )
    child = models.ForeignKey(
        Child, on_delete=models.PROTECT, related_name="lesson_progress"
    )
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.child} - {self.lesson}"


class ChildUnit(IdentifierTimeStampAbstractModel):
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="child_progress"
    )
    child = models.ForeignKey(
        Child, on_delete=models.PROTECT, related_name="unit_progress"
    )
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.child} - {self.unit}"


class ChildSubunit(IdentifierTimeStampAbstractModel):
    subunit = models.ForeignKey(
        Subunit, on_delete=models.CASCADE, related_name="child_progress"
    )
    child = models.ForeignKey(
        Child, on_delete=models.PROTECT, related_name="subunit_progress"
    )
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.child} - {self.subunit}"


class ChildCoursePreview(IdentifierTimeStampAbstractModel):
    course_preview = models.ForeignKey(
        CoursePreview, on_delete=models.PROTECT, related_name="child_progress"
    )
    child = models.ForeignKey(
        Child, on_delete=models.PROTECT, related_name="preview_progress"
    )
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.child} - {self.course_preview} - {'Complete' if self.completed else 'Incomplete'}"


class ChildCourseReview(IdentifierTimeStampAbstractModel):
    course_preview = models.ForeignKey(
        CourseReview, on_delete=models.PROTECT, related_name="child_progress"
    )
    child = models.ForeignKey(
        Child, on_delete=models.PROTECT, related_name="review_progress"
    )
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.child} - {self.course_preview} - {'Complete' if self.completed else 'Incomplete'}"
