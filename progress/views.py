from course.models import Course, Lesson, Subunit, Unit
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChildCourse, ChildSubunit
from .selectors import (course_progress_get, lesson_progress_get,
                        unit_progress_get)
from .serializers import CourseProgressSerializer
from .services import subunit_progress_create

# Tech debt: think about security.


# class ChildCourseProgressAPIView(RetrieveAPIView):
#     serializer_class = CourseProgressSerializer

#     def retrieve(self, request, *args, **kwargs):
#         serializer = self.serializer_class

#         child, course = request.query_params.get("child"), request.query_params.get(
#             "course"
#         )

#         total_subunits = Subunit.objects.filter(course__name=course).count()
#         print(total_subunits)
#         completed_subunits = ChildSubunit.objects.filter(
#             child__user__username=child, sub_unit__course__name=course
#         ).count()
#         print(completed_subunits)

#         progress = int((completed_subunits / total_subunits) * 100)
#         serializer = serializer(data={"progress": progress})
#         serializer.is_valid()

#         return Response(data=serializer.data, status=status.HTTP_200_OK)


class CourseProgressAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        course_name = request.query_params.get("course_name")
        try:
            progress_percentage = course_progress_get(
                user=request.user, course_name=course_name
            )
        except ValidationError as e:
            return Response(
                {"success": False, "message": e.message},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {"success": True, "data": {"progress_percentage": progress_percentage}},
            status=status.HTTP_200_OK,
        )


class LessonProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lesson_uid = request.query_params.get("lesson_uid")
        try:
            progress_percentage = lesson_progress_get(
                user=request.user, lesson_uid=lesson_uid
            )
        except ValidationError as e:
            return Response(
                {"success": False, "message": "No message for now"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {"success": True, "data": {"progress_percentage": progress_percentage}},
            status=status.HTTP_200_OK,
        )


class UnitProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    class UnitProgressInputSerializer(serializers.Serializer):
        unit_uid = serializers.CharField()

    class UnitProgressOutputSerializer(serializers.Serializer):
        progress_percentage = serializers.IntegerField()

    def get(self, request, *args, **kwargs):
        input_serializer = self.UnitProgressInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            progress_percentage = course_progress_get(
                user=request.user, **input_serializer.data
            )
        except ValidationError as e:
            return Response(
                {"success": False, "message": "No message for now."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        output_serializer = self.UnitProgressOutputSerializer(progress_percentage)
        return Response(
            {"success": True, "data": {"progress_percentage": progress_percentage}},
            status=status.HTTP_200_OK,
        )


class SubunitProgressCreateAPIView(APIView):
    class SubunitProgressCreateInputSerializer(serializers.Serializer):
        subunit_uid = serializers.UUIDField()

    def post(self, request, *args, **kwargs):
        input_serializer = self.SubunitProgressCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        
        if request.user.user_type == "guardian":
            return Response({"success": False, "message": "Invalid user type."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            subunit = subunit_progress_create(user=request.user, **request.data)
        except ValidationError as e:
            return Response({"success": False, "message": e.detail}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(
            {
                "success": True,
                "data": {"completed": True},
                "message": "Subunit completed successfully.",
            },
            status=status.HTTP_201_CREATED,
        )
