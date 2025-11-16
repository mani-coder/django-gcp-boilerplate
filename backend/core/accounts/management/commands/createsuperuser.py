# Django Imports
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    """
    Custom createsuperuser command that handles our User model
    which requires first_name and last_name fields.
    """

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--first_name",
            dest="first_name",
            default=None,
            help="Specifies the first name for the superuser.",
        )
        parser.add_argument(
            "--last_name",
            dest="last_name",
            default=None,
            help="Specifies the last name for the superuser.",
        )

    def handle(self, *args, **options):
        email = options.get("email")
        first_name = options.get("first_name")
        last_name = options.get("last_name")
        database = options.get("database")

        # If interactive mode, prompt for missing fields
        if options["interactive"]:
            if not email:
                email = self.get_input_data("email", "Email address: ")
            if not first_name:
                first_name = self.get_input_data("first_name", "First name: ", default="Admin")
            if not last_name:
                last_name = self.get_input_data("last_name", "Last name: ", default="User")

        # Validate required fields
        if not email:
            raise CommandError("Email is required")
        if not first_name:
            first_name = "Admin"
        if not last_name:
            last_name = "User"

        # Get password
        password = None
        if options["interactive"]:
            password = self._get_password()
            if not password:
                raise CommandError("Password is required")
        else:
            password = options.get("password")
            if not password:
                raise CommandError("Password is required in non-interactive mode")

        # Create the superuser
        try:
            user_data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
            }

            self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)

            if options["verbosity"] >= 1:
                self.stdout.write(f"Superuser created successfully.")
                self.stdout.write(f"Email: {email}")
                self.stdout.write(f"Name: {first_name} {last_name}")

        except Exception as e:
            raise CommandError(f"Error creating superuser: {e}")

    def get_input_data(self, field, message, default=None):
        """Get input data from user with optional default."""
        if default:
            message = f"{message}[{default}] "
        value = input(message)
        if not value and default:
            return default
        return value

    def _get_password(self):
        """Get password from user with validation."""
        import getpass

        password = None
        while password is None:
            password1 = getpass.getpass("Password: ")
            password2 = getpass.getpass("Password (again): ")

            if password1 != password2:
                self.stderr.write("Error: Your passwords didn't match.")
                password = None
                continue

            if not password1:
                self.stderr.write("Error: Blank passwords aren't allowed.")
                password = None
                continue

            password = password1

        return password
