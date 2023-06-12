from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AssessmentLogSerializer,
    AssessmentLogsInputSerializer,
    EquationSerializer,
    WordProblemSerializer,
)
from .services import generate_equation, word_problem
from .services.assessmentlog import assessment_log_create, generate_log_report
from .services.utils import random_integer


class GetAllEquationsAPIView(ListAPIView):
    serializer_class = EquationSerializer

    def get_queryset(self):
        return None

    def list(self, request, *args, **kwargs):
        """
        Returns all quizzes
        """
        level_one_equations = [generate_equation(level=1) for x in range(3)]
        level_two_equations = [generate_equation(level=2) for x in range(3)]
        level_three_equations = [generate_equation(level=3) for x in range(2)]
        level_four_equations = [generate_equation(level=4) for x in range(2)]

        equations = (
            level_one_equations
            + level_two_equations
            + level_three_equations
            + level_four_equations
        )
        serializer = self.serializer_class(data=equations, many=True)

        if serializer.is_valid(raise_exception=True):
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllWordProblemsAPIView(ListAPIView):
    serializer_class = WordProblemSerializer

    def get_queryset(self):
        return None

    def list(self, request, *args, **kwargs):
        """
        Returns all word problems
        """
        print("-" * 100)
        print("Printing request user")
        print(request.user)
        print("-" * 100)
        problem_set = [word_problem.generate(level=str(i)) for i in range(1, 5)]

        serializer = self.serializer_class(data=problem_set, many=True)

        if serializer.is_valid(raise_exception=True):
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAlgebraPostAssessmentsAPIView(APIView):
    equation_serializer = EquationSerializer
    word_problem_serializer = WordProblemSerializer

    def get(self, request, *args, **kwargs):
        """
        Returns 8 equations and 2 word problems.
        """
        equation_problem_set_one = [
            generate_equation(level=random_integer(min=1, max=2)) for i in range(4)
        ]
        equation_problem_set_two = [
            generate_equation(level=random_integer(min=3, max=4)) for i in range(4)
        ]

        word_problem_one = word_problem.generate(
            level=str(random_integer(min=1, max=2))
        )
        word_problem_two = word_problem.generate(
            level=str(random_integer(min=3, max=4))
        )

        equation_problem_set = equation_problem_set_one + equation_problem_set_two
        word_problem_set = [word_problem_one, word_problem_two]

        serialized_equations = self.equation_serializer(equation_problem_set, many=True)
        serialized_word_problems = self.word_problem_serializer(
            word_problem_set, many=True
        )

        return Response(
            {
                "success": True,
                "data": {
                    "equations": serialized_equations.data,
                    "word_problems": serialized_word_problems.data,
                },
            }
        )


class AssessmentLogsAPIView(APIView):
    serializer_class = AssessmentLogsInputSerializer

    def post(self, request, *args, **kwargs):

        input_serializer = self.serializer_class(data=request.data)
        print(input_serializer.initial_data)
        print()
        print("Printing request data...")
        print()
        print(request.data)

        input_serializer.is_valid(raise_exception=True)
        try:
            log_assessment = assessment_log_create(**input_serializer.data)
        except ValidationError as e:
            return Response(
                {"success": False, "message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response = Response(
            {
                "success": True,
                "message": "Child Assessment Log created.",
                "data": {"log_assessment": log_assessment},
            },
            status=status.HTTP_200_OK,
        )
        return response


class ChildLogsAPIView(APIView):
    serializer_class = AssessmentLogSerializer

    def get(self, request, *args, **kwargs):
        print("Printing request data...")
        print(request.query_params)
        username = request.query_params.get("child_username")
        course_name = request.query_params.get("course_name")

        log_report = generate_log_report(
            course_name=course_name, child_username=username
        )

        output_serializer = self.serializer_class(log_report, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_200_OK)
