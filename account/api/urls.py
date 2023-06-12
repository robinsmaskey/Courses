from django.urls import path

from .views import *

app_name = "account"

urlpatterns = [
    path("guardian/signup/", GuardianSignupAPIView.as_view(), name="guardian_signup"),
    path("guardian/login/", GuardianLoginAPIView.as_view(), name="login"),
    path("child/login/", ChildLoginAPIView.as_view(), name="child_login"),
    path(
        "child/signup/",
        ChildSignupAPIView.as_view(),
        name="child_signup",
    ),
    path("email/verify/", GuardianVerifyAPIView.as_view(), name="verify_email"),
    path("otp/resend/", ResendOtpAPIView.as_view(), name="verify_email"),
    path("child/list/", ChildListAPIView.as_view(), name="child_list"),
    path("user-details/", GetUserDetailsAPIView.as_view(), name="user_details"),
    path("token/refresh/", RotateAccessTokenAPIView.as_view(), name="refresh_token"),
    path("user/logout/", LogoutUserAPIView.as_view(), name="user_logout"),
    # path("otp/generate/", OtpGenerateAPIView.as_view(), name="generate_otp"),
    # path("email/verify", EmailVerifyAPIView.as_view(), name="verify_email"),
]
