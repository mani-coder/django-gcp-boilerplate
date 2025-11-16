# Third Party Library Imports
import graphene_django_optimizer
from graphene_django_optimizer.query import QueryOptimizer
from graphql.execution.execute import get_field_def


class CustomQueryOptimizer(QueryOptimizer):
    def optimize(self, queryset):
        info = self.root_info
        field_def = get_field_def(info.schema, info.parent_type, info.field_nodes[0])
        store = self._optimize_gql_selections(
            self._get_type(field_def),
            info.field_nodes[0],
            # info.parent_type,
        )
        return store.optimize_queryset(queryset)


def optimize_query(queryset, info, **options):
    return CustomQueryOptimizer(info, **options).optimize(queryset)


graphene_django_optimizer.query = optimize_query
