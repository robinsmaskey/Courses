from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course
from .nested_serializers import (AuthorizedNestedUnitOutputSerializer,
                                 RelatedNameListField,
                                 UnauthorizedNestedUnitOutputSerializer)
from .selectors import (course_preview_get_all, course_review_get_all,
                        get_adjacent_subunits_from_uid, get_all_courses,
                        get_all_lessons_from_course,
                        get_all_subunits_from_unit, get_all_units_from_lesson,
                        get_subunit_from_uid, lesson_get_from_uid,
                        next_subunit_get, previous_subunit_get)


class GetAllCoursesAPIView(APIView):

    # The nested serializer is in the nested_serializers.py folder.

    class GetAllCoursesOutputSerializer(serializers.ModelSerializer):
        lesson = RelatedNameListField(many=True, read_only=True)

        class Meta:
            model = Course
            ordering = ["created_date"]
            fields = ["uid", "name", "description", "subject", "lesson"]

    def get(self, request, *args, **kwargs):
        courses = get_all_courses()
        serializer = self.GetAllCoursesOutputSerializer(courses, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class GetLessonsFromCourseAPIView(APIView):
    class GetLessonsFromCourseOutputSerializer(serializers.Serializer):
        uid = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()

    class CoursePreviewOutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        type = serializers.CharField()
        link = serializers.URLField()
        completed = serializers.BooleanField(required=False)

    class CourseReviewOutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        type = serializers.CharField()
        link = serializers.URLField()
        text = serializers.CharField()
        completed = serializers.BooleanField(required=False)

    def get(self, request, *args, **kwargs):

        user = request.user
        course_name = request.query_params["course_name"]

        lessons = get_all_lessons_from_course(course_name=course_name)
        course_preview = course_preview_get_all(course_name=course_name, user=request.user)
        course_review = course_review_get_all(course_name=course_name, user=request.user)

        lesson_serializer = self.GetLessonsFromCourseOutputSerializer(
            lessons, many=True
        )
        preview_serializer = self.CoursePreviewOutputSerializer(
            course_preview, many=True
        )
        review_serializer = self.CourseReviewOutputSerializer(
            course_review, many=True
        )

        return Response(
            {
                "success": True,
                "data": {
                    "preview": preview_serializer.data,
                    "lesson": lesson_serializer.data,
                    "review": review_serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )


class GetUnitsFromLessonAPIView(APIView):
    class LessonDetailsOutputSerializer(serializers.Serializer):
        uid = serializers.UUIDField(read_only=True)
        name = serializers.CharField(read_only=True)
        description = serializers.CharField(read_only=True)

    def get(self, request, *args, **kwargs):

        user = request.user
        lesson_uid = request.query_params["lesson_uid"]

        units = get_all_units_from_lesson(lesson_uid=lesson_uid, user=user)

        if user.is_anonymous:
            units_serializer = UnauthorizedNestedUnitOutputSerializer(units, many=True)
        else:
            units_serializer = AuthorizedNestedUnitOutputSerializer(units, many=True)
        
        lesson = lesson_get_from_uid(uid=lesson_uid)
        if lesson is not None:
            lesson_serializer = self.LessonDetailsOutputSerializer(lesson)
            return Response(
                {
                    "success": True,
                    "data": {
                        "lesson": lesson_serializer.data,
                        "units": units_serializer.data,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": True, "message": "Lesson does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )


class GetSubunitsFromUnitAPIView(APIView):
    class GetSubunitsFromUnitOutputSerializer(serializers.Serializer):
        uid = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()

    def get(self, request, *args, **kwargs):
        unit_uid = request.query_params["unit_uid"]
        subunits = get_all_subunits_from_unit(unit_uid=unit_uid)
        serializer = self.GetSubunitsFromUnitOutputSerializer(subunits, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class GetSubunitLinkFromUid(APIView):
    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        link = serializers.URLField()
        type = serializers.CharField()

    def get(self, request, *args, **kwargs):
        subunit_uid = request.query_params["subunit_uid"]
        subunit = get_subunit_from_uid(uid=subunit_uid)
        if subunit is None:
            return Response(
                {"success": False, "message": "Subunit does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.OutputSerializer(subunit)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class GetAdjacentSubunitsFromUid(APIView):
    class SubunitOutputSerializer(serializers.Serializer):
        uid = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()

    def get(self, request, *args, **kwargs):

        subunit_uid = request.query_params["subunit_uid"]
        try:
            qset = get_adjacent_subunits_from_uid(uid=subunit_uid)
        except ValueError as e:
            return Response(
                {"success": False, "message": "Subunit does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.SubunitOutputSerializer(qset, many=True)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class GetNextSubunitFromUid(APIView):
    class SubunitOutputSerializer(serializers.Serializer):
        uid = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()
    
    def get(self, request, *args, **kwargs):
        subunit_uid = request.query_params.get("subunit_uid")
        if subunit_uid is None:
           return Response(
                {"success": False, "message": "Query parameter does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        subunit = next_subunit_get(current_subunit_uid=subunit_uid)
        if subunit is None:
             return Response(
                {"success": False, "message": "Subunit does not exist."},
                status=status.HTTP_200_OK,
            )
        serializer = self.SubunitOutputSerializer(subunit)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class GetPreviousSubunitFromUid(APIView):
    class SubunitOutputSerializer(serializers.Serializer):
        uid = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()
    
    def get(self, request, *args, **kwargs):
        subunit_uid = request.query_params.get("subunit_uid")
        if subunit_uid is None:
           return Response(
                {"success": False, "message": "Query parameter does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        subunit = previous_subunit_get(current_subunit_uid=subunit_uid)
        if subunit is None:
             return Response(
                {"success": False, "message": "Subunit does not exist."},
                status=status.HTTP_200_OK,
            )
        serializer = self.SubunitOutputSerializer(subunit)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )
