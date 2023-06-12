from django.urls import path

from .views import (
    AssessmentLogsAPIView,
    ChildLogsAPIView,
    GetAlgebraPostAssessmentsAPIView,
    GetAllEquationsAPIView,
    GetAllWordProblemsAPIView,
)

app_name = "assessment"

urlpatterns = [
    path(
        "quiz/post-assessment",
        GetAlgebraPostAssessmentsAPIView.as_view(),
        name="get_post_assessment_equations",
    ),
    path("quiz/equations", GetAllEquationsAPIView.as_view(), name="get_all_quizzes"),
    path(
        "quiz/word-problems",
        GetAllWordProblemsAPIView.as_view(),
        name="get_all_quizzes",
    ),
    path(
        "child/assessment/logs/",
        AssessmentLogsAPIView.as_view(),
        name="child_assessment_logs",
    ),
    path(
        "generate/report/logs/",
        ChildLogsAPIView.as_view(),
        name="generate_assessment_logs",
    ),
]
