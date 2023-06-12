from account.api.serializers import (ChildSerializer, EmailVerifySerializer,
                                     GuardianSerializer, ResendEmailSerializer)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ..permissions import IsGuardian, IsVerified
from ..selectors import guardian_child_list
from ..services import (child_login, child_signup, guardian_login,
                        guardian_signup, guardian_verify, otp_resend, otp_send)

User = get_user_model()


class GuardianSignupAPIView(APIView):
    class GuardianSignupInputSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)
        full_name = serializers.CharField(required=True)
        email = serializers.CharField(required=True)
        password = serializers.CharField(write_only=True, required=True)
        confirm_password = serializers.CharField(write_only=True, required=True)

    class GuardianSignupOutputSerializer(serializers.Serializer):
        user_type = serializers.CharField(read_only=True)
        username = serializers.CharField(read_only=True)
        full_name = serializers.CharField(read_only=True)
        email = serializers.EmailField(read_only=True)
        is_verified = serializers.CharField(read_only=True)
        access_token = serializers.CharField(read_only=True)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        input_serializer = self.GuardianSignupInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            guardian_signup_details, refresh_token = guardian_signup(
                **input_serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": e.detail[0],
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            otp = otp_send(guardian_email=guardian_signup_details.email)
        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": e.detail[0],
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        output_serializer = self.GuardianSignupOutputSerializer(guardian_signup_details)
        response = Response(
            {
                "success": True,
                "message": "Guardian sign up successful",
                "data": output_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        response.set_cookie(
            "refresh_token",
            refresh_token,
            max_age=settings.REFRESH_COOKIE_MAX_AGE,
            httponly=True,
            samesite="none",
            secure=True,
        )
        print("Refresh token set successfully.")
        print(refresh_token)

        return response


class GuardianLoginAPIView(APIView):
    class GuardianLoginInputSerializer(serializers.Serializer):
        username = serializers.CharField(write_only=True)
        password = serializers.CharField(write_only=True)

    class GuardianSLoginOutputSerializer(serializers.Serializer):
        user_type = serializers.CharField(read_only=True)
        username = serializers.CharField(read_only=True)
        full_name = serializers.CharField(read_only=True)
        is_verified = serializers.CharField(read_only=True)
        access_token = serializers.CharField(read_only=True)

    def post(self, request, *args, **kwargs):
        input_serializer = self.GuardianLoginInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            login_details, refresh_token = guardian_login(
                **input_serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": e.detail[0],
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        output_serializer = self.GuardianSLoginOutputSerializer(login_details)
        response = Response(
            {
                "success": True,
                "message": "Guardian log in successful.",
                "data": output_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            "refresh_token",
            refresh_token,
            max_age=settings.REFRESH_COOKIE_MAX_AGE,
            httponly=True,
            samesite="none",
            secure=True,
        )

        return response


class ChildSignupAPIView(APIView):
    # permission_classes = [IsAuthenticated, IsGuardian]

    class ChildSignupInputSerializer(serializers.Serializer):
        guardian_email = serializers.CharField()
        full_name = serializers.CharField()
        username = serializers.CharField()
        pin = serializers.CharField()
        confirm_pin = serializers.CharField()

    class ChildSignupOutputSerializer(serializers.Serializer):
        user_type = serializers.CharField()
        username = serializers.CharField()
        full_name = serializers.CharField()
        is_verified = serializers.BooleanField()
        access_token = serializers.CharField()

    def post(self, request, *args, **kwargs):
        input_serializer = self.ChildSignupInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        print(input_serializer.data)
        try:
            child_signup_details, refresh_token = child_signup(**input_serializer.data)
        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "message": e.detail[0],
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        output_serializer = self.ChildSignupOutputSerializer(child_signup_details)
        response = Response(
            {
                "success": True,
                "message": "Child added successfully.",
                "data": output_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            "refresh_token",
            refresh_token,
            max_age=settings.REFRESH_COOKIE_MAX_AGE,
            httponly=True,
            samesite="none",
            secure=True,
        )

        return response


class ChildLoginAPIView(APIView):
    class ChildLoginInputSerializer(serializers.Serializer):
        email = serializers.CharField(required=True)
        username = serializers.CharField(required=True)
        pin = serializers.CharField(required=True)

    class ChildLoginOutputSerializer(serializers.Serializer):
        user_type = serializers.CharField(read_only=True)
        username = serializers.CharField(read_only=True)
        full_name = serializers.CharField(read_only=True)
        is_verified = serializers.CharField(read_only=True)
        access_token = serializers.CharField(read_only=True)

    def post(self, request, *args, **kwargs):
        serializer = self.ChildLoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            child_login_details, refresh_token= child_login(
                **serializer.validated_data
            )
        except Exception as e:
            return Response(
                {
                    "success": True,
                    "message": e.detail[0],
                },
                status=status.HTTP_200_OK,
            )
        output_serializer = self.ChildLoginOutputSerializer(child_login_details)
        response = Response(
            {
                "success": True,
                "message": "Log in successful.",
                "data": output_serializer.data
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            "refresh_token",
            refresh_token,
            max_age=settings.REFRESH_COOKIE_MAX_AGE,
            httponly=True,
            samesite="none",
            secure=True,
        )
        return response


# Tech debt: request.user attribute has the username, no need to get user from access token.
class GetUserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    class UserDetailsOutputSerializer(serializers.Serializer):
        username = serializers.CharField()
        full_name = serializers.CharField()
        user_type = serializers.CharField()
        is_verified = serializers.BooleanField()

    def get(self, request, *args, **kwargs):

        serializer = self.UserDetailsOutputSerializer(request.user)
        return Response(
            {"success": True, "message": "Request Successful", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class LogoutUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        refresh_token = request.COOKIES["refresh_token"]
        if refresh_token is not None:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            return Response(
                {
                    "success": True,
                    "message": "Logout successful.",
                },
                status=status.HTTP_200_OK,
            )


class RotateAccessTokenAPIView(APIView):
    def get(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token is not None:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response(
                {
                    "success": True,
                    "message": "Token refreshed successfully.",
                    "data": {"access_token": access_token},
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "No refresh token",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class GuardianVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

    class GuardianVerifyInputSerializer(serializers.Serializer):
        otp = serializers.IntegerField()

    def post(self, request, *args, **kwargs):
        serializer = self.GuardianVerifyInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = guardian_verify(**serializer.data, user=request.user)
        except ValidationError as e:
            return Response(
                {"success": False, "message": e.detail},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "success": True,
                "message": "Guardian Verified Successfully.",
                "data": {"is_verified": user.is_verified},
            },
            status=status.HTTP_200_OK,
        )


class ResendOtpAPIView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

    def post(self, request, *args, **kwargs):
        print(request.user)
        try:
            otp = otp_resend(user=request.user)
        except ValidationError as e:
            return Response(
                {"success": False, "message": "Otp does not exist."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response({"success": True, "message": "Otp resent successfully."})


class ChildListAPIView(APIView):
    class GuardianChildOutputSerializer(serializers.Serializer):
        full_name = serializers.CharField(read_only=True)
        address = serializers.CharField(read_only=True)
        username = serializers.CharField(read_only=True)

    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        queryset = guardian_child_list(email=email)
        serializer = self.GuardianChildOutputSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
