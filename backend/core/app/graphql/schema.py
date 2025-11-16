# Third Party Library Imports
import graphene
from graphene_django.debug import DjangoDebug
from graphql_jwt import Refresh
from graphql_jwt import Verify

# App Imports
from accounts.gql.mutations.login import Login
from accounts.gql.resolver import get_user_query


class Query(graphene.ObjectType):
    # https://docs.graphene-python.org/projects/django/en/latest/debug/
    # This is used for viewing the SQL queries while running queries in graphiql.
    debug = graphene.Field(DjangoDebug, name="_debug")
    user = get_user_query()


class Mutations(graphene.ObjectType):
    login = Login.Field()

    # For mobile app to refresh & revoke the auth tokens.
    verify_auth_token = Verify.Field()
    refresh_auth_token = Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
