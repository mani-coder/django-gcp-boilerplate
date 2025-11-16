# Standard Library Imports
import math
import re
import unicodedata


def dict_lookup(obj, raw_path, default=None):
    """
    Get the value of the path in the dict.
    """
    if not obj:
        return default

    try:
        paths = raw_path.split(".")
        for path in paths:
            obj = obj[path]
            if obj is None:
                return default
        return obj
    except Exception:
        return default


def lookup(obj, raw_path, default=None):
    """
    Get the value of the path in the object.
    """
    try:
        paths = raw_path.split(".")
        for path in paths:
            obj = getattr(obj, path)
            if obj is None:
                return default
        return obj
    except Exception:
        return default


def sequencify(obj):
    if obj is None:
        return obj

    elif type(obj) in [list, tuple, set]:
        return obj

    else:
        return [obj]


def percentile(sorted_array, percent, key=lambda x: x):
    """
    Find the percentile of a list of values.
    Args:
    sorted_array - is a list of values. Note sorted_array MUST BE already sorted.
    percent - a float value from 0.0 to 1.0.
    key - optional key function to compute value from each element of sorted_array.

    Return
    The percentile of the values
    """
    if not sorted_array:
        return None

    k = (len(sorted_array) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(sorted_array[int(k)])
    d0 = key(sorted_array[int(f)]) * (c - k)
    d1 = key(sorted_array[int(c)]) * (k - f)
    return d0 + d1


def pluralize(value, term):
    return "{} {}s".format(value, term) if value > 1 else "{} {}".format(value, term)


def sanitize_url(url):
    """
    Remove additional slashes after http or https,
    like in http:////xyz.cdn.com/...
    """
    if not url:
        return None
    url = re.sub(r"(http[s]?:)([\/]{3,})", r"\1//", url)
    return url


def convert_to_ascii(string):
    return unicodedata.normalize("NFKD", string).encode("ascii", "ignore").decode("utf-8") if string else string


def dict_diff(dict1, dict2):
    diff_keys = [key for key in dict1 if dict1.get(key) != dict2.get(key)]
    return [(key, dict1.get(key), dict2.get(key)) for key in diff_keys]


def to_bool(value) -> bool:
    return value is not None and value in ["true", "True", "1"]
