#!/bin/sh

python manage.py collectstatic --no-input --clear
# Generate the new GQL schema.
python manage.py graphql_schema --out static/gql_schema.json

echo "Waiting for PSQL..."
while ! nc -z $POSTGRES_HOST 5432; do
  sleep 0.1
done
echo "PSQL started"

python manage.py migrate

exec "$@"
