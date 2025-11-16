# App Imports
from utils.enums import Enum
from utils.enums import EnumValue


ASYNC_TASK_HANDLER_URL_PREFIX = "api/tasks/async/"
CRON_TASK_HANDLER_URL_PREFIX = "api/tasks/crons/"


class TaskPayloadFields(Enum):
    TASK_ID = EnumValue("task_id", "Task ID")
    KWARGS = EnumValue("kwargs", "Keyword arguments")
    TASK_NAME = EnumValue("task_name", "Task Name")


class ServiceURLEnum(Enum):
    CORE = EnumValue("core", "https://core-473008725082.us-central1.run.app")
    WORKER = EnumValue("worker", "https://worker-473008725082.us-central1.run.app")


class QueueEnumValue(EnumValue):
    def __init__(self, value, verbose_name, target):
        self.target = target
        super(QueueEnumValue, self).__init__(value, verbose_name)


class QueuePriority(Enum):
    ASYNC_QUEUE = QueueEnumValue(
        value="async-tasks-queue",
        verbose_name="Background queue typically used for running cron jobs and delayed jobs.",
        target=ServiceURLEnum.verbose_name(ServiceURLEnum.WORKER),
    )
