from email.policy import default
from random import choices
from unittest.util import _MAX_LENGTH

from account.models import Child
from config.model_mixins import IdentifierTimeStampAbstractModel
from django.db import models
from django.utils.translation import gettext as _


class Course(IdentifierTimeStampAbstractModel):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=255, null=False)
    subject = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["created_date"]


class Lesson(IdentifierTimeStampAbstractModel):

    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, null=False, related_name="lesson"
    )
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-name"]


class Unit(IdentifierTimeStampAbstractModel):

    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, null=False, related_name="unit"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=False, related_name="unit"
    )
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-name"]


class Subunit(IdentifierTimeStampAbstractModel):
    class SubunitType(models.TextChoices):
        GAME = "GA", _("Game")
        VIDEO = "VD", _("Video")
        EPAATH = "EP", _("Epaath")

    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, null=False, related_name="subunit"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.PROTECT, null=False, related_name="subunit"
    )
    unit = models.ForeignKey(
        Unit, on_delete=models.PROTECT, null=False, related_name="subunit"
    )
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=255, null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(
        max_length=255,
        choices=SubunitType.choices,
        null=False,
        default=SubunitType.EPAATH,
    )

    def __str__(self) -> str:
        return self.name

    # class Meta:
    #     ordering = ["created_date"]


class CoursePreview(IdentifierTimeStampAbstractModel):
    class PreviewType(models.TextChoices):
        QUIZ = "Quiz", _("Quiz")
        VIDEO = "Video", _("Video")
        EPAATH = "Epaath", _("Epaath")

    class PreviewName(models.TextChoices):
        LESSON_INTRO = "Lesson Intro", _("Course Intro")
        PRE_ASSESSMENT = "Pre Assessment", _("Pre Assessment")

    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, null=False, related_name="preview"
    )
    name = models.CharField(max_length=255, choices=PreviewName.choices, null=False)
    type = models.CharField(max_length=255, choices=PreviewType.choices, null=False)
    link = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.course.name} - Preview"

    class Meta:
        ordering = ["-created_date"]


class CourseReview(IdentifierTimeStampAbstractModel):
    class ReviewType(models.TextChoices):
        QUIZ = "Quiz", _("Quiz")
        VIDEO = "Video", _("Video")
        EPAATH = "Epaath", _("Epaath")
        TEXT = "Text", _("Text")

    class ReviewName(models.TextChoices):
        POST_ASSESSMENT = "Post Assessment", _("Post Assessment")
        WHATS_NEXT = "What's Next?", _("What's Next?")

    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, null=False, related_name="review"
    )
    name = models.CharField(max_length=255, choices=ReviewName.choices, null=False)
    type = models.CharField(max_length=255, choices=ReviewType.choices, null=False)
    link = models.URLField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    completion_score = models.IntegerField(null=False, default=2)

    def __str__(self) -> str:
        return f"{self.course.name} - Review"

    class Meta:
        ordering = ["-created_date"]
