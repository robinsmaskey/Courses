from rest_framework import serializers
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model, password_validation
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
import re
from django.utils.translation import gettext_lazy as _
from account.models import Child
from django.utils import timezone
from ..models import Guardian


User = get_user_model()


class GuardianSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
            "email",
            "password",
            "confirm_password",
            "is_verified",
        )

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def validate_username(self, username):
        # alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
        # if 'username' not in alphanumeric:
        #    raise ValidationError('Please enter a valid username in alpha numeric values only.')
        if len(username) < 10:
            raise forms.ValidationError("username must contain 10 digits.")
        return username

    def validate(self, password, user=None):
        if not re.findall("[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]", str(password)):
            raise ValidationError(
                _(
                    "The password must contain at least 1 symbol: "
                    + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
                ),
                code="password_no_symbol",
            )
        return password

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 symbol: "
            + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class GuardianChildCreateSerializer(serializers.ModelSerializer):
    pin = serializers.IntegerField(required=True)
    confirm_pin = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("full_name", "username", "pin", "confirm_pin")

    def validate_pin(self, pin):
        pin = str(pin)
        if len(pin) == 4:
            return pin
        raise serializers.ValidationError("PIN must be 4 digit numbers.")

    def validate_username(self, username):
        # alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
        # if 'username' not in alphanumeric:
        #    raise ValidationError('Please enter a valid username in alpha numeric values only.')
        if len(username) < 10:
            raise forms.ValidationError("username must contain 10 digits.")
        return username

    def validate(self, attrs):
        if attrs["pin"] != attrs["confirm_pin"]:
            raise serializers.ValidationError({"pin": "PIN didn't match."})

        return attrs


# class OtpGenerateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Otp
#         fields = ["phone"]
#         extra_kwargs = {
#             'phone': {'validators': []},
#         }


# class OtpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Otp
#         fields = ["phone", "otp"]
#         extra_kwargs = {
#             'phone': {'validators': []},
#         }


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "username", "address", "phone")
        read_only_fields = ("id",)


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "address", "username")


class GuardianChildSerializer(serializers.Serializer):
    full_name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)


class ChildLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    pin = serializers.CharField(required=True)
