# Django-GCP Backend

Django backend for the Django-GCP boilerplate project with Cloud Run, Cloud SQL, Cloud Storage, Cloud Tasks, and WorkOS Authentication.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r dev-requirements.txt  # For development tools
```

### 2. Configure Environment

The project uses a layered environment configuration:

```bash
# Copy the secrets template
cp .env.dev.secrets.example .env.dev.secrets

# Edit .env.dev.secrets with your actual credentials
# - WORKOS_API_KEY and WORKOS_CLIENT_ID from https://dashboard.workos.com
# - SECRET_KEY (generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
```

**Note**: `.env.dev` already contains safe defaults and is committed to the repo. You only need to override secrets in `.env.dev.secrets`.

See [Environment Configuration](../../docs/ENVIRONMENT_CONFIG.md) for details.

### 3. Set Up Database

```bash
# Create PostgreSQL database
createdb django_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
# Using the dev script
./dev-server.sh

# Or manually
python manage.py runserver
```

Visit:
- Admin: http://localhost:8000/admin
- GraphiQL: http://localhost:8000/graphiql/

## Project Structure

```
backend/core/
├── app/                    # Main Django app (settings, URLs, ASGI/WSGI)
│   ├── settings.py        # Django settings with layered env loading
│   ├── urls.py            # URL routing
│   ├── graphql/           # GraphQL schema and views
│   └── templates/         # Django templates
├── accounts/              # User authentication with WorkOS
│   ├── models.py          # User model
│   ├── workos_auth.py     # WorkOS authentication module
│   └── gql/               # GraphQL mutations and queries
├── deploy/                # GCP deployment utilities
│   └── management/        # Django management commands
│       └── commands/
│           ├── deploy.py              # Deploy to Cloud Run
│           └── deploy_task_queues.py  # Deploy Cloud Tasks queues
├── tasks/                 # Cloud Tasks integration
│   ├── queue.py           # Task queue utilities
│   └── constants.py       # Queue configurations
├── utils/                 # Shared utilities
│   ├── auth/              # Authentication decorators
│   ├── graphql/           # GraphQL helpers
│   └── views/             # View helpers
├── .env.dev               # Committed: safe defaults
├── .env.dev.secrets       # Gitignored: your actual secrets
├── requirements.txt       # Production dependencies
├── dev-requirements.txt   # Development dependencies
├── Dockerfile             # Production Docker image
├── Dockerfile.dev         # Development Docker image
├── docker-compose.yml     # Local development with Docker
└── manage.py              # Django management script
```

## Development

### Running with Docker

```bash
# Start all services (Django + PostgreSQL)
docker-compose up

# Run migrations
docker-compose exec core python manage.py migrate

# Create superuser
docker-compose exec core python manage.py createsuperuser
```

### Management Commands

```bash
# Database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Deploy to GCP
python manage.py deploy

# Deploy Cloud Tasks queues
python manage.py deploy_task_queues
```

## Authentication

This project uses **WorkOS** for authentication with support for:
- Social login (Google, Microsoft, GitHub, etc.)
- Enterprise SSO (SAML, OAuth, OpenID Connect)
- Magic links (passwordless)
- Email/password

See [WorkOS Setup Guide](../../docs/WORKOS_SETUP.md) for configuration details.

## Deployment to GCP

### Prerequisites

1. **Install gcloud CLI**

   Follow the [official Google Cloud documentation](https://cloud.google.com/sdk/docs/install).

2. **Initialize gcloud**

   ```bash
   gcloud init
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Configure Docker for GCP**

   ```bash
   gcloud auth configure-docker us-central1-docker.pkg.dev
   ```

4. **Set up GCP resources**

   See [GCP Setup Guide](../../docs/GCP_SETUP.md) for detailed instructions.

### Deploy to Cloud Run

```bash
# Configure deployment settings in deploy/core.yaml
# Then deploy:
python manage.py deploy
```

### Deploy Cloud Tasks Queues

If you've added new task queues:

```bash
python manage.py deploy_task_queues
```

## Environment Configuration

The project uses a two-layer environment system:

1. **`.env.dev`** - Committed with safe defaults
2. **`.env.dev.secrets`** - Gitignored for actual credentials

### Key Environment Variables

**Base configuration (`.env.dev`):**
- `ENV` - Environment (dev/prod)
- `POSTGRES_*` - Database connection settings
- `GCP_PROJECT_ID` - Your GCP project
- `USE_GCS` - Enable Google Cloud Storage

**Secrets (`.env.dev.secrets`):**
- `SECRET_KEY` - Django secret key
- `WORKOS_API_KEY` - WorkOS API key
- `WORKOS_CLIENT_ID` - WorkOS client ID

See [Environment Configuration Guide](../../docs/ENVIRONMENT_CONFIG.md) for complete details.

## GraphQL API

The project includes a GraphQL API built with Graphene-Django.

### Access GraphiQL

Visit http://localhost:8000/graphiql/ to explore the API.

### Example Query

```graphql
query {
  me {
    id
    email
    firstName
    lastName
  }
}
```

### Example Mutation (Login)

```graphql
mutation {
  login(code: "workos_authorization_code") {
    responseCode
    token
    user {
      id
      email
      firstName
      lastName
    }
  }
}
```

## Cloud Tasks

Queue asynchronous tasks using Google Cloud Tasks:

```python
from tasks.queue import queue_async_task, TaskPayload

# Queue a task
queue_async_task(TaskPayload(
    function=my_function,
    kwargs={"arg1": "value1"},
    seconds=10  # delay in seconds
))
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Troubleshooting

### Database Connection Issues

Make sure PostgreSQL is running:
```bash
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Import Errors

Make sure you're in the virtual environment:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### WorkOS Authentication Errors

1. Check that `WORKOS_API_KEY` and `WORKOS_CLIENT_ID` are set in `.env.dev.secrets`
2. Verify the redirect URI matches your WorkOS dashboard configuration
3. Check the WorkOS dashboard for error logs

### GCP Deployment Issues

1. Ensure you're authenticated: `gcloud auth login`
2. Check project is set: `gcloud config get-value project`
3. Verify Docker is configured: `gcloud auth configure-docker`

## Additional Resources

- [Main README](../../README.md)
- [Environment Configuration](../../docs/ENVIRONMENT_CONFIG.md)
- [WorkOS Setup](../../docs/WORKOS_SETUP.md)
- [GCP Setup](../../docs/GCP_SETUP.md)
- [Deployment Guide](../../docs/DEPLOYMENT.md)
- [Customization Guide](../../docs/CUSTOMIZATION.md)

## License

MIT License - see [LICENSE](../../LICENSE) file for details.
