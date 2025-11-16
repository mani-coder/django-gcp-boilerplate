# Third Party Library Imports
from graphql.utilities import ast_to_dict
from inflection import underscore


def _collect_fields(node, fragments, ignore_typename):
    fields = {}

    if node.get("selection_set"):
        for leaf in node["selection_set"]["selections"]:
            if leaf["kind"] == "field":
                field = underscore(leaf["name"]["value"])
                if ignore_typename and field == "__typename":
                    continue

                fields.update({field: _collect_fields(leaf, fragments, ignore_typename)})

            elif leaf["kind"] == "fragment_spread":
                fields.update(_collect_fields(fragments[leaf["name"]["value"]], fragments, ignore_typename))

    return fields


def get_gql_fields(info, ignore_typename=True):
    """
    Recursively collects fields from the AST

    Args:
        node (dict): A node in the AST
        fragments (dict): Fragment definitions

    Returns:
        A dict mapping each field found, along with their sub fields.
        {'name': {},
         'sentimentsPerLanguage': {'id': {},
                                   'name': {},
                                   'totalSentiments': {}},
         'slug': {}}
    """
    fragments = {}

    node = ast_to_dict(info.field_nodes[0])

    for name, value in info.fragments.items():
        fragments[name] = ast_to_dict(value)

    return _collect_fields(node, fragments, ignore_typename)
