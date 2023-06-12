from django.urls import path

from .views import (GetAdjacentSubunitsFromUid, GetAllCoursesAPIView,
                    GetLessonsFromCourseAPIView, GetNextSubunitFromUid,
                    GetPreviousSubunitFromUid, GetSubunitLinkFromUid,
                    GetSubunitsFromUnitAPIView, GetUnitsFromLessonAPIView)

app_name = "course"

urlpatterns = [
    path("all/", GetAllCoursesAPIView.as_view(), name="all_courses"),
    path("lessons/", GetLessonsFromCourseAPIView.as_view(), name="all_lessons"),
    path("subunits/", GetSubunitsFromUnitAPIView.as_view(), name="all_subunits"),
    path("units/", GetUnitsFromLessonAPIView.as_view(), name="all_units"),
    path("subunit/link/", GetSubunitLinkFromUid.as_view(), name="subunit_link"),
    path("subunit/next/", GetNextSubunitFromUid.as_view(), name="subunit_link"),
    path("subunit/previous/", GetPreviousSubunitFromUid.as_view(), name="subunit_link"),
    path(
        "subunit/adjacent/",
        GetAdjacentSubunitsFromUid.as_view(),
        name="subunit_adjacent",
    ),
]
