# Standard Library Imports
import logging

# Third Party Library Imports
from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from graphene_django.views import GraphQLView
from graphql.error.graphql_error import GraphQLError
from graphql.error.syntax_error import GraphQLSyntaxError

# App Imports
from utils.graphql.exceptions import format_graphql_error
from utils.graphql.exceptions import format_internal_error


logger = logging.getLogger(__name__)


class CustomGraphQLView(GraphQLView):
    @staticmethod
    def format_error(error):
        try:
            if isinstance(error, GraphQLSyntaxError):
                return error.formatted

            if isinstance(error, GraphQLError):
                return format_graphql_error(error)

        except Exception as e:
            return format_internal_error(e)


class GraphiQLView(AccessMixin, CustomGraphQLView):
    def __init__(self, **kwargs):
        super().__init__(graphiql=True, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not settings.DEBUG and not request.user.is_superuser:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
