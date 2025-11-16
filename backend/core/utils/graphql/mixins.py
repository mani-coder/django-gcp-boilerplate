# Standard Library Imports
import logging

# Third Party Library Imports
import graphene


logger = logging.getLogger(__name__)


class IntIdMixin(graphene.ObjectType):
    id = graphene.NonNull(graphene.Int)


class History(graphene.ObjectType):
    history_id = graphene.NonNull(graphene.Int)
    history_date = graphene.NonNull(graphene.DateTime)
    history_type = graphene.NonNull(graphene.String)
    history_user_id = graphene.Int()


class HistoryMixin(graphene.ObjectType):
    history = graphene.List(graphene.NonNull(History))

    def resolve_history(self, info):
        return self.history.all()
