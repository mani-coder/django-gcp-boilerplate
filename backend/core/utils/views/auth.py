# Django Imports
# Third Party Library Imports
from django.contrib.auth.mixins import LoginRequiredMixin


class StaffMixin(LoginRequiredMixin):
    """
    Verify that the current user is staff.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
