# Standard Library Imports

# Third Party Library Imports
from django.core.management.base import BaseCommand

# App Imports
from deploy.management.base import AbstractBaseCommand


class Command(BaseCommand, AbstractBaseCommand):
    help = "Deploy the tasks queue config."

    def add_arguments(self, parser):
        AbstractBaseCommand.add_base_arguments(parser)

    def handle(self, *args, **kwargs):
        self.print_alert("Deploying task queues!")
        self.handle_terraform_deploy(module="queues", dry_run=kwargs.get("dry_run"))
        self.print_alert("Task queue deploy completed.\n\n")
