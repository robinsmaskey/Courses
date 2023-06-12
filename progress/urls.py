from django.urls import path

from .views import (
    CourseProgressAPIView,
    LessonProgressAPIView,
    SubunitProgressCreateAPIView,
    UnitProgressAPIView,
)

app_name = "progress"

get_requests_urlpatterns = [
    path("course/", CourseProgressAPIView.as_view(), name="course_progress"),
    path("lesson/", LessonProgressAPIView.as_view(), name="lesson_progress"),
    path("unit/", UnitProgressAPIView.as_view(), name="unit_progress"),
]

post_request_urlpatterns = [
    path(
        "subunit/complete/",
        SubunitProgressCreateAPIView.as_view(),
        name="Subunit progress create.",
    )
]

urlpatterns = get_requests_urlpatterns + post_request_urlpatterns
