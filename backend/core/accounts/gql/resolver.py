# Third Party Library Imports
import graphene

# App Imports
from accounts.gql.schema import User
from accounts.models import User as UserModel
from utils.graphql.query_optimizer import optimize_query


def get_user_query():
    def resolve_user(root, info, **kwargs):
        if not info.context.user.is_authenticated:
            return

        return optimize_query(UserModel.objects.filter(id=info.context.user.id)[:1], info)[0]

    return graphene.Field(lambda: User, resolver=resolve_user)
