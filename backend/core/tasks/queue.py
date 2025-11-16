# Standard Library Imports
import logging
import pickle
import uuid
from datetime import datetime
from datetime import timedelta
from typing import Optional

# Third Party Library Imports
from google.api_core.exceptions import DeadlineExceeded
from google.cloud import tasks_v2
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2
from pydantic import BaseModel

# Same App Imports
from .constants import ASYNC_TASK_HANDLER_URL_PREFIX
from .constants import QueuePriority
from .constants import TaskPayloadFields

# Project Imports
from app.settings import DEBUG
from app.settings import GCP_PROJECT_ID
from app.settings import GCP_REGION


logger = logging.getLogger(__name__)
TASK_TIMEOUT_DURATION = duration_pb2.Duration(seconds=30 * 60)


class TaskPayload(BaseModel):
    function: callable
    kwargs: Optional[dict] = {}
    seconds: Optional[int] = 0
    queue: QueuePriority = QueuePriority.ASYNC_QUEUE


def queue_async_task(payload: TaskPayload):
    """
    Queue the given task to run asynchronously in our async queue.
    """
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project=GCP_PROJECT_ID, location=GCP_REGION, queue=payload.queue)
    task_id = str(uuid.uuid4().hex) + str(uuid.uuid4().hex)

    if DEBUG:
        if callable(payload.function):
            payload.function(**payload.kwargs)
        return

    task_name = payload.function
    if callable(payload.function):
        task_name = "{}.{}".format(payload.function.__module__, payload.function.__name__)

    target_url = QueuePriority.enum_value(payload.queue).target

    task = {
        "name": f"{parent}/tasks/{task_id}",
        "dispatch_deadline": TASK_TIMEOUT_DURATION,
        "http_request": {
            "http_method": "POST",
            "url": "{}/{}{}".format(target_url, ASYNC_TASK_HANDLER_URL_PREFIX, task_name),
            # todo: use service account email.
            # "oidc_token": {"service_account_email": ""},
            "body": pickle.dumps(
                {
                    TaskPayloadFields.TASK_ID: task_id,
                    TaskPayloadFields.TASK_NAME: task_name,
                    TaskPayloadFields.KWARGS: payload.kwargs,
                }
            ),
        },
    }

    if payload.seconds:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(datetime.now() + timedelta(seconds=payload.seconds))
        task["schedule_time"] = timestamp

    logger.info(f"Publishing task_id: {task_id} to task queue: {payload.queue}")

    try:
        response = client.create_task(parent=parent, task=task)
    except DeadlineExceeded:
        response = client.create_task(parent=parent, task=task)

    return response
