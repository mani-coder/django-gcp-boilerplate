# App Imports
from utils.enums import Enum
from utils.enums import EnumValue


class PermissionEnumValue(EnumValue):
    def __init__(self, value, verbose_name, user_field=None):
        self.user_field = user_field
        return super().__init__(value, verbose_name)


class Permission(Enum):
    IS_LOGGED_IN = PermissionEnumValue("is_logged_in", "Logged In", "is_authenticated")
    IS_SUPERUSER = PermissionEnumValue("is_superuser", "Superuser", "is_superuser")
    IS_STAFF = PermissionEnumValue("is_staff", "Staff", "is_staff")


SPECIAL_PERMISSIONS = {Permission.IS_LOGGED_IN, Permission.IS_SUPERUSER, Permission.IS_STAFF}

PERMISSIONS = {perm.split(".")[1] for perm in set(Permission.values()) - SPECIAL_PERMISSIONS}

SPECIAL_PERMISSION_TO_USER_FIELD = {perm: Permission.enum_value(perm).user_field for perm in SPECIAL_PERMISSIONS}

PERMISSION_TO_VERBOSE_NAME = {perm: Permission.verbose_name(perm) for perm in Permission.values()}
