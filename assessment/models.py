from tabnanny import verbose

from account.models import Child
from config.model_mixins import IdentifierTimeStampAbstractModel
from course.models import Course
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# class Assessment(IdentifierTimeStampAbstractModel):

#     class AssessmentType(models.TextChoices):
#         PRE = "PR", _("Pre assessment")
#         POST = "PO", _("Post assessment")
#     name = models.CharField(max_length=255)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assessment")
#     assessment_type = models.CharField(
#         max_length=2, null=True, choices=AssessmentType.choices
#     )

#     def __str__(self) -> str:
#         return self.name

#     class Meta:
#         ordering = ["uid"]
#         verbose_name = "Assessment"
#         verbose_name_plural = "Assessments"


class ChildAssessmentLog(IdentifierTimeStampAbstractModel):
    class AssessmentType(models.TextChoices):
        PRE = "PR", _("Pre assessment")
        POST = "PO", _("Post assessment")

    class AssessmentLevel(models.TextChoices):
        ONE = "1", _("1")
        TWO = "2", _("2")
        THREE = "3", _("3")
        FOUR = "4", _("4")

    class QuestionType(models.TextChoices):
        EQUATIONS = "EQ", _("Equations")
        WORD_PROBLEMS = "WP", _("Word Problems")

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="assessment_log"
    )
    child = models.ForeignKey(
        Child, on_delete=models.CASCADE, related_name="assessment_log"
    )
    assessment_type = models.CharField(
        max_length=2, default="PO", choices=AssessmentType.choices, null=False
    )
    assessment_level = models.CharField(
        max_length=2, choices=AssessmentLevel.choices, null=False
    )
    question_type = models.CharField(
        max_length=10, choices=QuestionType.choices, null=False
    )
    number_of_attempts = models.IntegerField(null=True)
    number_of_correct = models.IntegerField(null=True)
    number_of_incorrect = models.IntegerField(null=True)
    number_of_skips = models.IntegerField(null=True)

    class Meta:
        ordering = ["-updated_date"]

    def __str__(self) -> str:
        return f"{self.course} - {self.child}"
