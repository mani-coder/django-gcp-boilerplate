# Standard Library Imports
import base64
import json
from datetime import date
from datetime import datetime


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f+00:00"
DATE_FORMAT = "%Y-%m-%d"


def jsonify(obj, use_datetime_decoder=False):
    if obj and isinstance(obj, str):
        if use_datetime_decoder:
            return json.loads(obj, object_hook=DateTimeDecoder.object_hook)
        else:
            return json.loads(obj)

    return obj


def dumpify(obj, use_datetime_encoder=False):
    if not obj:
        return obj

    if not isinstance(obj, str):
        if use_datetime_encoder:
            return json.dumps(obj, cls=DateTimeEncoder)

    return obj


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return datetime.strftime(obj, DATETIME_FORMAT)

        if isinstance(obj, date):
            return date.strftime(obj, DATE_FORMAT)

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def get_datetime_obj(value):
    try:
        return datetime.strptime(value, DATETIME_FORMAT)
    except Exception:
        pass

    try:
        return datetime.strptime(value, DATE_FORMAT).date()
    except Exception:
        pass


class DateTimeDecoder(object):
    @staticmethod
    def object_hook(data):
        for key, value in data.items():
            if isinstance(value, str):
                value = get_datetime_obj(value)
                if value:
                    data[key] = value

        return data


def json_to_base64(data):
    """
    Convert a JSON object to a Base64-encoded string.

    Args:
        data (dict): The JSON object to be encoded.

    Returns:
        str: The Base64-encoded representation of the JSON object.
    """
    # Convert the JSON object to a string
    json_str = json.dumps(data)

    # Convert the string to bytes
    json_bytes = json_str.encode("utf-8")

    # Encode the byte array to Base64
    base64_bytes = base64.b64encode(json_bytes)

    # Convert Base64 bytes back to a string
    base64_str = base64_bytes.decode("utf-8")

    return base64_str
