# Standard Library Imports
import logging

# App Imports
from utils.graphql.exceptions import PermissionDenied


logger = logging.getLogger(__name__)


class ErrorLoggingMiddleware(object):
    def resolve(self, next, root, info, **args):
        try:
            return next(root, info, **args)
        except PermissionDenied as e:
            # raise permission denied errors to UI.
            raise e
        except Exception as e:
            logger.exception(
                "[Graphql Error] Graphql execution failed with errors: {}".format(str(e)),
            )
            raise e
