# Third Party Library Imports
# Django Imports
# Third Party Library Imports
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    def create_superuser(self, email: str, first_name: str, last_name: str, password: str):
        user: User = self.model(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            workos_user_id=email,  # For superuser, use email as placeholder
        )
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

    def __str__(self):
        return f"{self.id} {self.email}"
