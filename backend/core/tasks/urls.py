# Standard Library Imports
import logging

# Third Party Library Imports
from django.urls import path

# Same App Imports
from .constants import ASYNC_TASK_HANDLER_URL_PREFIX
from .constants import CRON_TASK_HANDLER_URL_PREFIX

# App Imports
from tasks.views import async_tasks_handler
from tasks.views import cron_task_handler


logger = logging.getLogger(__name__)


urlpatterns = [
    path(f"{CRON_TASK_HANDLER_URL_PREFIX}<slug:task_name>/", cron_task_handler, name="cron_handler"),
    path(f"{ASYNC_TASK_HANDLER_URL_PREFIX}<slug:task_name>/", async_tasks_handler, name="async_task_handler"),
]
