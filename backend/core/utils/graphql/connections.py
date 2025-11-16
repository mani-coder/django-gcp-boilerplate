# Third Party Library Imports
import graphene
from graphene.relay import Connection
from graphene.utils.str_converters import to_snake_case
from graphene_django.filter import DjangoFilterConnectionField

# App Imports
from utils.commons import sequencify


class CountableConnection(Connection):
    total_count = graphene.NonNull(graphene.Int)

    class Meta:
        abstract = True

    # Method returns a value of you want to add parameters
    def resolve_total_count(self, info):
        return self.length


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    @staticmethod
    def parse_order_field(field):
        return to_snake_case(field) if isinstance(field, str) else field.value

    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):
        order = args.get("order", None)
        qs = DjangoFilterConnectionField.resolve_queryset(
            connection, iterable, info, args, filtering_args, filterset_class
        )
        if not order:
            return qs

        return qs.order_by(*map(cls.parse_order_field, sequencify(order)))
