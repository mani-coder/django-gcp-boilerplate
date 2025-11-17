# Django-GCP Boilerplate

A production-ready Django boilerplate for Google Cloud Platform (GCP) with Cloud Run, Cloud SQL, Cloud Storage, Cloud Tasks, and WorkOS Authentication.

## Features

- ✅ **Django 5.1** - Latest stable Django version
- ✅ **Google Cloud Run** - Serverless deployment with auto-scaling
- ✅ **Cloud SQL (PostgreSQL)** - Managed PostgreSQL database
- ✅ **Cloud Storage** - Static and media file storage
- ✅ **Cloud Tasks** - Async job queue processing
- ✅ **Cloud Logging** - Centralized logging
- ✅ **WorkOS Authentication** - Enterprise-ready authentication with SSO (free for 1M users)
- ✅ **GraphQL API** - GraphQL API with Graphene-Django
- ✅ **Docker Support** - Docker and docker-compose for local development
- ✅ **Custom Deploy Commands** - Django management commands for easy deployment
- ✅ **Environment-based Configuration** - Easy configuration management

## Project Structure

```
django-gcp-boilerplate/
├── backend/
│   └── core/                       # Django backend application
│       ├── app/                    # Main Django app (settings, URLs, ASGI/WSGI)
│       ├── accounts/               # User authentication & WorkOS integration
│       │   ├── models.py           # User model with WorkOS integration
│       │   ├── workos_auth.py      # WorkOS authentication utilities
│       │   └── gql/                # GraphQL schema (mutations, queries)
│       ├── deploy/                 # GCP deployment utilities
│       │   ├── management/         # Custom deploy commands
│       │   └── terraform/          # Terraform configs for Cloud Tasks
│       ├── tasks/                  # Cloud Tasks integration
│       ├── utils/                  # Shared utilities
│       ├── Dockerfile              # Production Docker image
│       ├── Dockerfile.dev          # Development Docker image
│       ├── docker-compose.yml      # Local development with Docker
│       ├── requirements.txt        # Python dependencies
│       ├── dev-requirements.txt    # Development dependencies
│       ├── .env.dev                # Base env config (committed)
│       ├── .env.dev.secrets        # Secret overrides (gitignored)
│       └── manage.py               # Django management script
│
├── frontend/
│   └── console/                    # React admin console (Vite + TypeScript)
│       ├── src/
│       │   ├── components/         # React components
│       │   │   └── ProtectedRoute.tsx
│       │   ├── pages/              # Page components
│       │   │   ├── Login.tsx       # WorkOS OAuth login
│       │   │   ├── AuthCallback.tsx # OAuth callback handler
│       │   │   └── Dashboard.tsx   # Main dashboard
│       │   ├── lib/                # Utilities
│       │   │   ├── graphql-client.ts # urql client setup
│       │   │   ├── auth.ts         # Auth utilities
│       │   │   └── utils.ts        # shadcn/ui utilities
│       │   ├── graphql/            # GraphQL operations
│       │   │   └── mutations.ts    # Login mutation
│       │   ├── __generated__/      # Auto-generated types (gitignored)
│       │   └── gql/                # Downloaded schema (gitignored)
│       ├── public/                 # Static assets (favicons, etc.)
│       ├── package.json            # Node dependencies
│       ├── vite.config.ts          # Vite configuration
│       ├── tailwind.config.js      # Tailwind CSS config
│       ├── codegen.ts              # GraphQL codegen config
│       ├── codegen-schema.yml      # Schema download config
│       ├── .env                    # Frontend env vars
│       ├── .nvmrc                  # Node version (24 LTS)
│       └── README.md               # Frontend documentation
│
├── infra/
│   ├── favicon/                    # App favicon assets
│   └── README.md                   # Infrastructure documentation
│
├── docs/                           # Documentation
│   ├── ENVIRONMENT_CONFIG.md       # Environment setup guide
│   ├── WORKOS_SETUP.md            # WorkOS configuration
│   ├── DEPLOYMENT.md              # GCP deployment guide
│   └── GCP_SETUP.md               # GCP initial setup
│
├── CLAUDE.md                       # AI-assisted development guide
├── CONTRIBUTING.md                 # Development workflow
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 16
- Docker & Docker Compose (optional, for containerized development)
- Google Cloud SDK (for GCP deployment)
- WorkOS account (for authentication - free for 1M users)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/django-gcp-boilerplate.git
cd django-gcp-boilerplate/backend/core

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

### 2. Configure Environment

The project uses a two-file environment setup:
- `.env.dev` - Committed with safe defaults (already in repo)
- `.env.dev.secrets` - Gitignored file for your actual credentials

```bash
# Copy the secrets template
cd backend/core
cp .env.dev.secrets.example .env.dev.secrets

# Edit .env.dev.secrets with your actual credentials:
# - SECRET_KEY (generate a secure one)
# - WORKOS_API_KEY and WORKOS_CLIENT_ID (from WorkOS dashboard)
# - GCP_PROJECT_ID (your actual GCP project)
```

**Note**: The base `.env.dev` is committed to the repository with safe defaults. You only need to override the secrets you actually need in `.env.dev.secrets`.

### 3. Database Setup

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
# Start development server
./dev-server.sh

# Or manually:
python manage.py runserver
```

Visit `http://localhost:8000/admin` to access the Django admin panel.

### 5. Run Frontend Console (Optional)

The project includes a React-based admin console for internal staff:

```bash
cd frontend/console

# Use Node 24 LTS
nvm use  # Reads from .nvmrc

# Install dependencies
npm install

# Start dev server
npm run dev
```

Visit `http://localhost:3000` to access the admin console.

See [`frontend/console/README.md`](frontend/console/README.md) for detailed frontend documentation.

## Docker Development

```bash
# Start all services (Django + PostgreSQL)
docker-compose up

# Run migrations in container
docker-compose exec core python manage.py migrate

# Create superuser in container
docker-compose exec core python manage.py createsuperuser
```

## Deployment to GCP

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy

```bash
# 1. Setup GCP (first time only)
# See docs/GCP_SETUP.md

# 2. Configure deployment
# Edit backend/core/deploy/core.yaml with your GCP project details

# 3. Deploy
cd backend/core
python manage.py deploy
```

## Configuration

### Environment Variables

The project uses a layered environment configuration:

1. **`.env.dev`** (committed) - Contains safe defaults for local development
2. **`.env.dev.secrets`** (gitignored) - Override with your actual credentials
3. **`.env.prod`** (production) - Production settings (use GCP Secret Manager)

Key variables to override in `.env.dev.secrets`:
- `SECRET_KEY`: Django secret key (generate a secure one)
- `WORKOS_API_KEY`: WorkOS API key from dashboard
- `WORKOS_CLIENT_ID`: WorkOS Client ID from dashboard
- `GCP_PROJECT_ID`: Your actual GCP project ID

Optional overrides:
- `POSTGRES_*`: Database credentials (if different from defaults)
- `OPENAI_API_KEY`: If you need OpenAI integration

See `.env.dev` for all available variables and `.env.dev.secrets.example` for the template.

### WorkOS Setup

1. Create a free WorkOS account at https://workos.com
2. Create a new organization and environment
3. Get your API Key and Client ID from the dashboard
4. Configure your redirect URI (e.g., `http://localhost:8000/auth/callback`)

See [docs/WORKOS_SETUP.md](docs/WORKOS_SETUP.md) for details.

## GraphQL API

Access GraphiQL interface at `http://localhost:8000/graphiql/`

Example query:
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

## Cloud Tasks

The boilerplate includes Cloud Tasks integration for async job processing.

```python
from tasks.queue import queue_async_task, TaskPayload

# Queue a task
queue_async_task(TaskPayload(
    function=my_function,
    kwargs={"arg1": "value1"},
    seconds=10  # delay in seconds
))
```

## Custom Django Apps

To add your own Django app:

```bash
# Create new app
python manage.py startapp myapp

# Add to INSTALLED_APPS in app/settings.py
INSTALLED_APPS = [
    ...
    "myapp",
]
```

## Development Commands

```bash
# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Deploy to GCP
python manage.py deploy

# Deploy Cloud Tasks queues
python manage.py deploy_task_queues
```

## Documentation

- [Environment Configuration](docs/ENVIRONMENT_CONFIG.md) - Understanding the env file structure
- [GCP Setup Guide](docs/GCP_SETUP.md)
- [WorkOS Setup](docs/WORKOS_SETUP.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Customization Guide](docs/CUSTOMIZATION.md)

## Tech Stack

- **Backend**: Django 5.1, Python 3.12
- **Database**: PostgreSQL 16
- **API**: GraphQL (Graphene-Django), REST (Django REST Framework)
- **Authentication**: WorkOS (SSO, OAuth, User Management), JWT
- **Cloud**: Google Cloud Run, Cloud SQL, Cloud Storage, Cloud Tasks
- **Server**: Uvicorn (ASGI), Gunicorn
- **Storage**: django-storages (GCS integration)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation in `docs/`

## Acknowledgments

This boilerplate was created to help developers quickly deploy Django applications to Google Cloud Platform with production-ready configurations.
