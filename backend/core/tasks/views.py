# Standard Library Imports
import logging
import pickle
import time
from importlib import import_module

# Third Party Library Imports
from django.http import HttpResponse

# Same App Imports
from .constants import TaskPayloadFields


logger = logging.getLogger(__name__)


def cron_task_handler(request, task_name):
    if request.headers.get("X-CloudScheduler") != "true":
        return HttpResponse("Forbidden", status=403)

    logger.info("Handling the cron tasks handler invocation for task: {}".format(task_name))

    duration = _run_task(task_name)

    logger.info("Handled the cron tasks handler for task: {}, duration: {:.3f}s".format(task_name, duration))

    return HttpResponse("OK")


def async_tasks_handler(request, task_name):
    if request.headers.get("X-CloudTasks-QueueName") is None:
        return HttpResponse("Forbidden", status=403)

    body = pickle.loads(request.body)
    task_id = body.get(TaskPayloadFields.TASK_ID, "ID")
    logger.info(f"[{task_id}] Handling the async tasks handler invocation for task: {task_name}")

    task_kwargs = body.get(TaskPayloadFields.KWARGS, {})

    duration = _run_task(task_name, **task_kwargs)

    logger.info(
        "[{}] Handled the async tasks handler for task: {}, duration: {:.3f}s".format(task_id, task_name, duration)
    )

    return HttpResponse("OK")


def _run_task(task_name, **kwargs):
    module_name = ".".join(task_name.split(".")[:-1])
    task_function_name = task_name.split(".")[-1]
    module = import_module(module_name)

    logger.info(
        "Running task, module: {}, function_name: {}, params: {}".format(module_name, task_function_name, kwargs)
    )

    start_time = time.time()
    getattr(module, task_function_name)(**kwargs)
    end_time = time.time()

    return end_time - start_time
