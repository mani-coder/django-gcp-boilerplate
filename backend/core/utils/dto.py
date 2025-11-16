# Standard Library Imports
from operator import attrgetter

# Third Party Library Imports
# Django Imports
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor

# App Imports
from utils.commons import lookup


def convert_to_dto(db_object, dto_class):
    def _get_field_value(field):
        model_field = lookup(db_object._meta.model, field)
        value = lookup(db_object, field)
        if value is not None:
            if isinstance(model_field, ReverseManyToOneDescriptor):
                return list(map(attrgetter("dto"), value.all()))
            else:
                dto = lookup(value, "dto")
                return dto if dto else value
        else:
            return value

    return dto_class(**{field: _get_field_value(field) for field in dto_class.__dataclass_fields__})


def as_dict(dto):
    return dto.__dict__
