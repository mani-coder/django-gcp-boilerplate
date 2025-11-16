# Third Party Library Imports
from django.forms import IntegerField
from django_filters.filters import NumberFilter


class IntegerFilter(NumberFilter):
    field_class = IntegerField
