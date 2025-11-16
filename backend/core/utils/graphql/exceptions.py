# Standard Library Imports
import logging
import traceback

# Third Party Library Imports
#
# Django Imports
from django.conf import settings
from graphql.error import GraphQLError

# Same App Imports
from ..commons import lookup
from .str_converters import dict_key_to_camel_case
from .str_converters import to_kebab_case


logger = logging.getLogger(__name__)


class CustomGraphQLError(GraphQLError):
    message = "An error occurred"

    def __init__(self, message=None, *args, **kwags):
        if message is None:
            message = self.message
        super().__init__(message, *args, **kwags)


class PermissionDenied(CustomGraphQLError):
    message = "You do not have permission to perform this action"


class ResponseError(Exception):
    def __init__(self, message, code=None, params=None):
        super().__init__(message)
        self.message = str(message)
        self.code = code
        self.params = params


def encode_code(code):
    if code is None:
        return None
    return to_kebab_case(code)


def encode_params(params):
    if params is None:
        return None
    return dict_key_to_camel_case(params)


def format_permission_error(error: PermissionDenied):
    result = {
        "message": error.message,
        "code": "permission-denied",
    }

    if settings.DEBUG:
        result["trace"] = traceback.format_list(traceback.extract_tb(error.__traceback__))

    return result


def format_response_error(error: ResponseError):
    return {
        "message": error.message,
        "code": encode_code(error.code),
        "params": encode_params(error.params),
    }


def format_internal_error(error: Exception):
    message = "Internal server error"
    code = "internal-server-error"

    return {
        "code": code,
        "message": message,
        "params": {
            "exception": type(error).__name__,
            "message": str(error),
            "trace": traceback.format_list(traceback.extract_tb(error.__traceback__)),
        },
    }


def format_graphql_error(error):
    original_error = lookup(error, "original_error")
    if isinstance(original_error, ResponseError):
        return format_response_error(error)

    elif isinstance(original_error, PermissionDenied):
        return format_permission_error(error)

    elif isinstance(error, GraphQLError):
        logger.exception(
            "[Graphql Error] Graphql execution failed with errors: {}".format(str(error)),
            exc_info=error,
        )

        data = dict(**error.formatted)
        data.update(
            {
                "code": "graphql-error",
                "params": {
                    "exception": type(error).__name__,
                    "message": str(error),
                    "trace": traceback.format_list(traceback.extract_tb(error.__traceback__)),
                },
            }
        )
        return data

    return format_internal_error(error)
