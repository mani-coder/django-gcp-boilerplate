# Django Imports
# Third Party Library Imports
from django.contrib import admin

# Same App Imports
from .models import User


admin.site.register(User)
