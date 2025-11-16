# Standard Library Imports
import datetime
import json

# Third Party Library Imports
from graphene import DateTime
from graphene import JSONString
from graphene.types.datetime import Date


class JSON(JSONString):
    """
    JSON
    """

    @staticmethod
    def serialize(dt):
        return json.loads(dt) if dt and isinstance(dt, str) else dt.to_dict() if hasattr(dt, "to_dict") else dt

    @staticmethod
    def parse_value(value):
        return json.loads(value) if value and isinstance(value, str) else value


class DateOrDateTime(DateTime):
    @staticmethod
    def parse_value(value):
        if isinstance(value, datetime.date):
            return Date.parse_value(value)

        return DateTime.parse_value(value)
