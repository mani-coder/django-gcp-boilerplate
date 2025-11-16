from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError("The Email field must be set")

        # Ensure first_name and last_name have defaults
        if "first_name" not in extra_fields or not extra_fields["first_name"]:
            extra_fields["first_name"] = "Admin"
        if "last_name" not in extra_fields or not extra_fields["last_name"]:
            extra_fields["last_name"] = "User"

        # Use email as workos_user_id placeholder for superusers
        if "workos_user_id" not in extra_fields:
            extra_fields["workos_user_id"] = email

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    email = models.EmailField(verbose_name=_("email address"), max_length=255, unique=True, null=False)
    workos_user_id = models.CharField(max_length=255, null=False, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=False)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        null=False,
        help_text=_("Designates whether this user should be treated as active. "),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        null=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    created_at = models.DateTimeField(_("created at"), default=timezone.now)
    modified_at = models.DateTimeField(_("modified at"), default=timezone.now)

    history = HistoricalRecords()

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.id} {self.email}"
