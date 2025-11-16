# Standard Library Imports
from itertools import chain
from operator import attrgetter
from typing import List

# Third Party Library Imports
import graphene

# App Imports
from utils.commons import lookup
from utils.enums import Enum


def get_gql_enum(enum_cls: Enum, name=None):
    name = name if name else enum_cls.__name__
    return graphene.Enum(
        name,
        map(attrgetter("__name__", "value"), enum_cls.enum_values_it()),
    )


def get_gql_enum_for_list(enums: List[Enum], name):
    return graphene.Enum(
        name,
        chain(*[map(attrgetter("__name__", "value"), enum_cls.enum_values_it()) for enum_cls in enums]),
    )


def get_enum_value(value):
    return lookup(value, "value", default=value)


def get_enum(enum_cls, value):
    try:
        return enum_cls.get(value)
    except Exception:
        pass
