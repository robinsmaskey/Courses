from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from reward.models import Reward


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, username, password, **extra_fields)


class PortalUser(AbstractUser):
    alphanumeric = RegexValidator(
        r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed."
    )
    USER_TYPES = (
        ("child", "child"),
        ("guardian", "guardian"),
    )
    username = models.CharField(max_length=100, validators=[alphanumeric], unique=True)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=64, null=True, blank=True)
    user_type = models.CharField(choices=USER_TYPES, max_length=64)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to="media/images/user/")
    objects = UserManager()
    USERNAME_FIELD = "username"

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return self.username


class Child(models.Model):
    user = models.ForeignKey(PortalUser, on_delete=models.CASCADE, related_name="child")
    total_points = models.IntegerField(blank=True, null=True)
    rewards = models.ManyToManyField(Reward)

    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"

    def __str__(self):
        return self.user.username


class Guardian(models.Model):
    user = models.ForeignKey(
        PortalUser, on_delete=models.CASCADE, related_name="guardian"
    )
    email = models.EmailField(unique=True)
    children = models.ManyToManyField(Child)

    class Meta:
        verbose_name = "Guardian"
        verbose_name_plural = "Guardian"

    def __str__(self):
        return self.user.username


class Otp(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otp"
    )
    otp = models.CharField(max_length=6)
    created_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
        ordering = ["-created_time"]

    def __str__(self) -> str:
        return self.otp

    @property
    def has_expired(self) -> bool:
        now = timezone.now()
        created_time = self.created_time + timedelta(minutes=5)
        return now > created_time
