# Standard Library Imports
import json

# Third Party Library Imports
import yaml
from django.core.management.base import BaseCommand

# Project Imports
from deploy.management.base import AbstractBaseCommand
from app.settings import GCP_PROJECT_ID
from app.settings import GCP_REGION


class Command(BaseCommand, AbstractBaseCommand):
    help = "Deploy the backend core service."
    service = "core"

    def add_arguments(self, parser):
        AbstractBaseCommand.add_base_arguments(parser)
        parser.add_argument(
            "--beta", action="store_true", dest="beta", default=False, help="Specify if this is a beta deployment"
        )
        parser.add_argument(
            "--use_cloud_build",
            action="store_true",
            dest="use_cloud_build",
            default=False,
            help="Specify if you want to use cloud build for deployment",
        )

    def deploy(self, beta_deploy: bool = False, dry_run: bool = False, use_cloud_build: bool = False):
        service = self.service
        if not beta_deploy:
            self.print_header("Pulling latest main")
            command = "git pull origin main"
            self.run_command(command, dry_run)
            self.print("Pulled lastest main")

        if use_cloud_build:
            self.print_header("Building base image in cloud deploy")
            command = f"gcloud builds submit --project={GCP_PROJECT_ID} --config=deploy/cloudbuild.yaml"
            self.run_command(command, dry_run)
        else:
            self.print_header("Building base image in local")
            self.print("Build Docker image")
            command = f"docker build -t us-central1-docker.pkg.dev/{GCP_PROJECT_ID}/deploy/{service} ."
            self.run_command(command, dry_run)
            self.print()
            self.print("Pushing image to GCR")
            command = f"docker push us-central1-docker.pkg.dev/{GCP_PROJECT_ID}/deploy/{service}"
            self.run_command(command, dry_run)

        self.print_header("Triggering deploy.")
        command = f"gcloud run deploy {service} --project {GCP_PROJECT_ID}"
        service_config = yaml.load(open(f"deploy/{service}.yaml"), Loader=yaml.FullLoader)
        for key, value in service_config.items():
            if not isinstance(value, dict):
                if key == "flags":
                    command += "".join([f" --{x} " for x in value.split(",")])
                else:
                    command += f" --{key}={value} "
            else:
                command += f" --{key}={','.join([f'{x}={value[x]}' for x in value])}"

        if beta_deploy:
            command += "  --no-traffic  --tag=beta"

        self.run_command(command, dry_run)
        self.print_success(f"Deployed {service}\n")

        if not beta_deploy:
            command = f"gcloud run services describe {service} --project {GCP_PROJECT_ID} --region={GCP_REGION} --format=json"
            deploy_output = self.run_command(command, dry_run, capture_output=True)
            if dry_run:
                self.print("Using dummy output from command..")
                deploy_output = {
                    "traffic": [{"latestRevision": True, "percent": 100, "revisionName": "core-00000-xyz"}],
                    "latestCreatedRevisionName": "core-00001-xyz",
                }
            else:
                deploy_output = json.loads(deploy_output.stdout)["status"]

            traffic = deploy_output["traffic"][0]
            latest_revision_name = deploy_output["latestCreatedRevisionName"]

            # To handle traffic migrated manually in console
            if latest_revision_name != traffic["revisionName"]:
                self.print_header(f"Migrating traffic to latest {service}")
                command = f"gcloud run services update-traffic {service} --to-latest --region={GCP_REGION} --project={GCP_PROJECT_ID}"
                self.run_command(command, dry_run)

        self.print()

    def handle(self, *args, **kwargs):
        self.print_alert(f"Starting deployment to {self.service} service")
        self.deploy(
            beta_deploy=kwargs.get("beta"),
            dry_run=kwargs.get("dry_run"),
            use_cloud_build=kwargs.get("use_cloud_build"),
        )
        self.print_alert("Deployment completed successfully!")
        self.print()
