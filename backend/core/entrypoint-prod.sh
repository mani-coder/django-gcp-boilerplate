#!/bin/bash

python manage.py migrate
python manage.py collectstatic --no-input --clear
# Generate the new GQL schema.
python manage.py graphql_schema --out static/gql_schema.json

exec "$@"
