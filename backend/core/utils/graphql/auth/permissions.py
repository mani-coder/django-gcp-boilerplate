# Django Extensions
# Third Party Library Imports
#
# Django Imports
# Third Party Library Imports
from django.contrib.auth.models import AbstractUser
from graphene_django import DjangoObjectType
from graphene_django.types import DjangoObjectTypeOptions

# Same App Imports
from ..exceptions import PermissionDenied
from ..query_optimizer import optimize_query

# App Imports
from utils.commons import sequencify


class PermissionedDjangoObjectTypeOptions(DjangoObjectTypeOptions):
    perms = set()
    optimize_query = False
    branch_field = None
    allow_all_branches = None


class PermissionedDjangoObjectType(DjangoObjectType):
    @classmethod
    def __init_subclass_with_meta__(
        cls,
        perms=None,
        optimize_query=None,
        branch_field=None,
        allow_all_branches=None,
        _meta=None,
        **options,
    ):
        assert bool(perms), "Configure permissions for {}".format(options.get("model").__name__)

        if not _meta:
            _meta = PermissionedDjangoObjectTypeOptions(cls)
        _meta.perms = set(sequencify(perms)) if perms else set()
        _meta.optimize_query = bool(optimize_query)
        _meta.branch_field = branch_field
        _meta.allow_all_branches = bool(allow_all_branches)

        super().__init_subclass_with_meta__(_meta=_meta, **options)

    class Meta:
        abstract = True

    @classmethod
    def get_queryset(cls, queryset, info):
        user: AbstractUser = info.context.user
        if not user:
            raise PermissionDenied

        if not user.has_perms(cls._meta.perms):
            raise PermissionDenied

        if cls._meta.optimize_query:
            return optimize_query(super().get_queryset(queryset, info), info)
        else:
            return super().get_queryset(queryset, info)
