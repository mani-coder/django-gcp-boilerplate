# Standard Library Imports
import calendar
import json
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta


TWO_DAYS = timedelta(days=2)
ONE_DAY = timedelta(days=1)


def parse_datetime(datetime_str):
    """
    Parse the given date string to a date object.

    :param datetime_str: Date time string.
    :return: datetime object, if we can successfully parse it else None.
    """
    if not datetime_str:
        return

    if isinstance(datetime_str, datetime):
        return datetime_str

    if isinstance(datetime_str, date):
        return datetime(datetime_str.year, datetime_str.month, datetime_str.day)

    for date_format in [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f+00:00",
        "%Y-%m-%d@%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%m-%d-%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
    ]:
        try:
            return datetime.strptime(datetime_str, date_format)
        except Exception:
            pass

    return parse_datetime(parse_date(datetime_str))


def parse_date(date_str):
    """
    Parse the given date string to a date object.

    :param date_str: Date string.
    :return: Date object, if we can successfully parse it else None.
    """
    if not date_str:
        return

    if isinstance(date_str, date):
        return date_str

    if isinstance(date_str, datetime):
        return date_str.date()

    parsed_datetime = None
    for date_format in ["%Y-%m-%d", "%Y/%m/%d", "%m-%d-%Y", "%m/%d/%Y"]:
        try:
            parsed_datetime = datetime.strptime(date_str, date_format)
            break
        except Exception:
            pass

    return parsed_datetime.date() if parsed_datetime else None


def get_first_of_current_or_next_month(effective_date):
    """
    Get the first day of next month. If 1st, return the 1st of current month

    :return: First day of month
    """
    if effective_date.day == 1:
        return effective_date
    return effective_date.replace(day=1) + timedelta(months=1)


def get_end_of_month(date_obj):
    """
    Get the end of the month.

    :param date_obj: Date object.
    :return: End of the month date.
    """
    return date_obj.replace(day=1) + timedelta(months=1, days=-1)


def format_readable_date(date_str, format_mask):
    d = parse_date(date_str)
    if d:
        return d.strftime(format_mask)
    else:
        return date_str


def format_iso_date(date_string):
    return format_readable_date(date_string, "%Y-%m-%d")


def format_masked_date(date_string):
    return format_readable_date(date_string, "**/**/%Y")


def format_local_month(date_string):
    return format_readable_date(date_string, "%B")


def format_date(date_string):
    return format_readable_date(date_string, "%b %d, %Y")


def format_long_date(date_string):
    return format_readable_date(date_string, "%B %d, %Y")


def get_effective_dates_it(dtstart, dtend, rd):
    """
    Get the effective dates between two given dates based on the relative delta.

    :param dtstart: Date start.
    :param dtend: Date end.
    :param rd: Relative delta object.
    :return: Iterator to the effective dates.
    """
    ii = 0
    while True:
        cdate = dtstart + ii * rd
        ii += 1

        if cdate > dtend:
            break

        yield cdate


def get_utc_epoch_time(date_str):
    dt = parse_datetime(date_str)
    if not dt:
        return

    return int(calendar.timegm(dt.timetuple()) * 1e3 + dt.microsecond / 1e6)


def parse_datetime_with_utc_offset(t):
    ret = datetime.strptime(t[0:16], "%Y-%m-%dT%H:%M")
    if t[18] == "+":
        ret += timedelta(hours=int(t[19:22]), minutes=int(t[23:]))
    elif t[18] == "-":
        ret -= timedelta(hours=int(t[19:22]), minutes=int(t[23:]))
    return ret


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()

        elif isinstance(obj, timedelta):
            return (datetime.min + obj).time().isoformat()

        return super().default(obj)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.date().isoformat()

        elif isinstance(obj, date):
            return obj.isoformat()

        return super().default(obj)
