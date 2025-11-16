# Django Imports
# Third Party Library Imports
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import floatformat

# App Imports
from utils.datetime import format_date as _format_date


register = template.Library()


@register.filter
def format_date(value):
    return _format_date(value)


@register.filter
def currency(value):
    if not value:
        return "--"

    value = round(float(value), 2)
    return "₹%s%s" % (intcomma(int(value)), ("%0.2f" % value)[-3:])


@register.filter
def percent(value):
    if not value:
        return "--"

    return f"{floatformat(value * 100, 2)}%"
