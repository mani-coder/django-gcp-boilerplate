# Standard Library Imports
import subprocess
import sys
from abc import ABC


class Colors(object):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class AbstractBaseCommand(ABC):
    @classmethod
    def add_base_arguments(cls, parser):
        parser.add_argument(
            "--dry_run",
            action="store_true",
            dest="dry_run",
            default=False,
            help="Specify if you want to do a dry run and generate the commands.",
        )

    def print(self, message=""):
        self.stdout.write(message)

    def print_header(self, message):
        self.print("\n\n")
        self.print(Colors.BOLD + Colors.UNDERLINE + Colors.OKCYAN + message + Colors.ENDC)

    def print_success(self, message):
        self.print(Colors.OKGREEN + message + Colors.ENDC)

    def print_info(self, message):
        self.print(Colors.OKBLUE + message + Colors.ENDC)

    def print_alert(self, message):
        self.stdout.write(self.style.WARNING(message))

    def print_failure(self, message, exit=True):
        self.print(Colors.BOLD + Colors.FAIL + message + Colors.ENDC)
        if exit:
            sys.exit(1)

    def run_command(self, command, dry_run=False, capture_output=False):
        self.print_info(f"> {command}")
        if not dry_run:
            return subprocess.run(command.split(), check=True, capture_output=capture_output)

    def handle_terraform_deploy(self, module, dry_run=False):
        self.print_header(f"Running terraform deploy for {module}")
        base_command = "terraform -chdir=deploy/terraform/queues"
        for command in ["init", "validate", "apply", "plan"]:
            self.run_command(f"{base_command} {command}", dry_run=dry_run)
            self.print()
