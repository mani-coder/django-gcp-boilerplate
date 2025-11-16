# Django Imports
# Third Party Library Imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test


permission_required_api = permission_required
login_required_api = login_required


def superuser_required_api(function=None):
    """
    Decorator for views that checks that the user is logged in and is superuser,
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(lambda u: u.is_authenticated and u.is_superuser)
    return actual_decorator(function) if function else actual_decorator


def staff_member_required_api(function=None):
    """
    Decorator for views that checks that the user is logged in and is staff,
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(lambda u: u.is_authenticated and u.is_staff)
    return actual_decorator(function) if function else actual_decorator
