# Third Party Library Imports
import graphene

# Django Imports
from django.contrib.auth.models import Group as GroupModel
from django.contrib.auth.models import Permission as PermissionModel
from django.contrib.contenttypes.models import ContentType as ContentTypeModel

# Django Extensions
from graphene_django.types import DjangoObjectType
from graphene_django_optimizer import resolver_hints

# Same App Imports
from ..models import User as UserModel

# App Imports
from utils.auth.constants import PERMISSION_TO_VERBOSE_NAME
from utils.auth.constants import Permission as PermissionEnum
from utils.graphql.enum import get_gql_enum
from utils.graphql.mixins import IntIdMixin


PermissionGQLEnum = get_gql_enum(PermissionEnum, "PermissionEnum")


class Permission(DjangoObjectType, IntIdMixin):
    permission_enum = graphene.Field(PermissionGQLEnum)
    permission = graphene.Field(graphene.NonNull(graphene.String))
    description = graphene.Field(graphene.NonNull(graphene.String))

    class Meta:
        model = PermissionModel
        exclude = ("user_set", "group_set")

    @resolver_hints(
        only=("codename", "content_type__app_label"),
        select_related=("content_type",),
    )
    def resolve_permission(root, info):
        return f"{root.content_type.app_label}.{root.codename}"

    @resolver_hints(
        only=("codename", "name", "content_type__app_label"),
        select_related=("content_type",),
    )
    def resolve_description(root, info):
        permission = f"{root.content_type.app_label}.{root.codename}"
        if permission in PERMISSION_TO_VERBOSE_NAME:
            return PERMISSION_TO_VERBOSE_NAME[permission]

        else:
            return root.name

    @resolver_hints(
        only=("codename", "content_type__app_label"),
        select_related=("content_type",),
    )
    def resolve_permission_enum(root, info):
        permission = f"{root.content_type.app_label}.{root.codename}"
        try:
            PermissionEnum.validate_value(permission)
            return permission
        except Exception:
            pass


class Group(DjangoObjectType, IntIdMixin):
    class Meta:
        model = GroupModel
        exclude = ("user_set",)


class ContentType(DjangoObjectType, IntIdMixin):
    class Meta:
        model = ContentTypeModel
        exclude = ("permission_set",)


class User(DjangoObjectType, IntIdMixin):
    class Meta:
        model = UserModel
        exclude = ["password"]
