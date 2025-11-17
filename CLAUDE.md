# Claude AI Development Guide

This document helps you (or any AI assistant like Claude) quickly understand and work with this Django-GCP boilerplate project.

## Project Overview

**Django-GCP Boilerplate** is a production-ready full-stack application template with:
- **Backend**: Django 5.1 + GraphQL + WorkOS Auth
- **Frontend**: React 19 + Vite 7 + TypeScript + Tailwind CSS
- **Infrastructure**: Google Cloud Platform (Cloud Run, Cloud SQL, Cloud Storage, Cloud Tasks)

## Quick Setup for AI Development

### 1. Understanding the Codebase

**Project Root**: `/django-gcp-boilerplate/`

```
Key Directories:
├── backend/core/          # Django application
├── frontend/console/      # React admin console
├── docs/                  # Documentation
└── infra/                 # Infrastructure assets
```

### 2. Backend (Django)

**Location**: `backend/core/`

**Key Files**:
- `app/settings.py` - Django settings (WorkOS config at bottom)
- `accounts/workos_auth.py` - WorkOS authentication module
- `accounts/gql/mutations/login.py` - Login GraphQL mutation
- `requirements.txt` - Python dependencies
- `.env.dev` - Base environment (committed)
- `.env.dev.secrets` - Secret overrides (gitignored)

**Tech Stack**:
- Django 5.1, Python 3.12
- PostgreSQL 16
- GraphQL (Graphene-Django)
- WorkOS 5.32.0 for auth
- JWT tokens
- Cloud Tasks for async jobs

**Important Patterns**:
1. **Settings from Django conf**: Always use `from django.conf import settings` and `settings.WORKOS_*` instead of `os.environ.get()`
2. **Two-layer env config**: `.env.dev` (committed) + `.env.dev.secrets` (gitignored)
3. **Auto-reload**: Uses `watchfiles` for fast file watching

**Running Backend**:
```bash
cd backend/core
python manage.py runserver  # Auto-reloads on code changes
```

### 3. Frontend (React Console)

**Location**: `frontend/console/`

**Key Files**:
- `src/pages/` - Page components (Login, AuthCallback, Dashboard)
- `src/lib/graphql-client.ts` - urql GraphQL client
- `src/lib/auth.ts` - Auth utilities (WorkOS redirect, token management)
- `src/graphql/mutations.ts` - GraphQL operations
- `vite.config.ts` - Vite config (port 3000)
- `codegen.ts` - GraphQL type generation
- `.nvmrc` - Node version (24 LTS)

**Tech Stack**:
- React 19.2, TypeScript 5.9, Node 24 LTS
- Vite 7.2 (runs on port 3000)
- Tailwind CSS 4.1
- urql 5.0 (GraphQL client)
- React Router 7.9
- shadcn/ui utilities
- GraphQL Code Generator

**Important Patterns**:
1. **Path aliases**: Use `@/*` imports (configured in vite.config.ts and tsconfig)
2. **GraphQL codegen**: Run `npm run codegen` after schema changes
3. **Environment vars**: Prefix with `VITE_` (e.g., `VITE_GRAPHQL_URL`)

**Running Frontend**:
```bash
cd frontend/console
nvm use              # Uses Node 24 from .nvmrc
npm run dev          # Runs on http://localhost:3000
```

**GraphQL Type Generation**:
```bash
npm run genschema    # Fetch schema from backend
npm run gentypes     # Generate TypeScript types
npm run codegen      # Both commands
```

### 4. Authentication Flow

**WorkOS OAuth Flow**:
1. Frontend redirects to WorkOS OAuth (`/login`)
2. User authenticates with WorkOS
3. WorkOS redirects back with code (`/auth/callback?code=...`)
4. Frontend calls GraphQL `login` mutation with code
5. Backend validates code with WorkOS SDK
6. Backend returns JWT token
7. Frontend stores token in localStorage
8. Protected routes check for token

**Key Environment Variables**:
- Backend: `WORKOS_API_KEY`, `WORKOS_CLIENT_ID`
- Frontend: `VITE_WORKOS_CLIENT_ID`, `VITE_WORKOS_REDIRECT_URI`

### 5. Common Development Tasks

#### Adding a New GraphQL Mutation

**Backend** (`backend/core/accounts/gql/mutations/`):
```python
import graphene
from django.conf import settings

class MyMutation(graphene.Mutation):
    class Arguments:
        input_field = graphene.String(required=True)

    result = graphene.String()

    def mutate(self, info, input_field):
        # Your logic here
        return MyMutation(result="Success")
```

**Frontend** (`frontend/console/src/graphql/mutations.ts`):
```typescript
export const MY_MUTATION = gql`
  mutation MyMutation($inputField: String!) {
    myMutation(inputField: $inputField) {
      result
    }
  }
`
```

Then regenerate types: `npm run codegen`

#### Adding a New Page

1. Create component in `frontend/console/src/pages/NewPage.tsx`
2. Add route in `frontend/console/src/App.tsx`:
```typescript
<Route path="/newpage" element={<NewPage />} />
```

#### Using WorkOS Client

**Backend** (`backend/core/accounts/workos_auth.py`):
```python
from django.conf import settings
from workos import WorkOSClient

client = WorkOSClient(
    api_key=settings.WORKOS_API_KEY,
    client_id=settings.WORKOS_CLIENT_ID,
)

# Authenticate with code
auth_response = client.user_management.authenticate_with_code(code=code)
user = auth_response.user
```

**Note**: Don't pass `client_id` to `authenticate_with_code()` - it's configured on the client instance.

#### Debugging Tips

**Backend Logs**:
```bash
# Django auto-prints logs to console with watchfiles
# Look for ERROR/INFO statements in the terminal
```

**Frontend Network Requests**:
- Open Chrome DevTools → Network tab
- Filter by "graphql" to see API calls
- Check Response tab for GraphQL errors

**Common Issues**:
1. **CORS errors**: Check `corsheaders.middleware.CorsMiddleware` is in MIDDLEWARE
2. **WorkOS auth fails**: Check client_id parameter isn't being passed
3. **GraphQL types outdated**: Run `npm run codegen`

### 6. Database Operations

**Create Migration**:
```bash
cd backend/core
python manage.py makemigrations
python manage.py migrate
```

**Access Database**:
```bash
# Django shell
python manage.py shell

# PostgreSQL directly
psql django_db
```

### 7. Code Style & Formatting

**Backend**:
- Follow Django conventions
- Use type hints where possible
- Import order: Standard → Third-party → Django → Local

**Frontend**:
```bash
npm run format      # Format with Prettier
npm run lint        # ESLint + TypeScript checks
npm run style       # Both format + lint:fix
```

### 8. Environment Variables Reference

**Backend** (`.env.dev.secrets`):
```bash
SECRET_KEY=your-secret-key
WORKOS_API_KEY=sk_test_...
WORKOS_CLIENT_ID=client_...
GCP_PROJECT_ID=your-project-id
```

**Frontend** (`.env`):
```bash
VITE_GRAPHQL_URL=http://localhost:8000/graphql/
VITE_WORKOS_CLIENT_ID=client_...
VITE_WORKOS_REDIRECT_URI=http://localhost:3000/auth/callback
```

### 9. Useful Commands

**Backend**:
```bash
python manage.py runserver          # Run dev server
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin user
python manage.py shell              # Django shell
python manage.py test               # Run tests
```

**Frontend**:
```bash
npm run dev         # Start dev server
npm run build       # Build for production
npm run codegen     # Generate GraphQL types
npm run format      # Format code
npm run lint        # Check code quality
```

### 10. Project Conventions

1. **Use Django settings for config**: `from django.conf import settings`
2. **WorkOS SDK**: Client ID configured on client instance, not in method calls
3. **Frontend imports**: Use `@/` alias for src imports
4. **GraphQL**: Keep mutations in `graphql/mutations.ts`, queries in `graphql/queries.ts`
5. **Environment**: Two-layer system (base + secrets)
6. **Node version**: Always use Node 24 LTS (`.nvmrc`)
7. **Auto-reload**: Both frontend and backend watch for file changes

### 11. Testing Your Changes

**Backend**:
```bash
# Start server
python manage.py runserver

# Test GraphQL in browser
open http://localhost:8000/graphiql/
```

**Frontend**:
```bash
# Start dev server
npm run dev

# Test in browser
open http://localhost:3000
```

**Full Stack Test** (Login Flow):
1. Start backend: `python manage.py runserver`
2. Start frontend: `npm run dev`
3. Visit `http://localhost:3000`
4. Click login → should redirect to WorkOS
5. Authenticate → should redirect back and show dashboard

## AI Development Best Practices

When helping with this project:

1. **Always read relevant files** before making changes
2. **Check existing patterns** in the codebase
3. **Update both backend and frontend** when changing GraphQL schema
4. **Run codegen** after GraphQL changes: `npm run codegen`
5. **Test the change** by running both servers
6. **Follow the project structure** - don't create new directories unnecessarily
7. **Use Django settings** instead of direct `os.environ` access
8. **Keep documentation updated** when adding features

## Quick Reference

**Backend Entry Point**: `backend/core/manage.py`
**Frontend Entry Point**: `frontend/console/src/main.tsx`
**GraphQL Schema**: Auto-generated at `frontend/console/src/gql/schema.graphql`
**Settings**: `backend/core/app/settings.py`
**Auth Module**: `backend/core/accounts/workos_auth.py`

## Getting Help

- **Documentation**: Check `docs/` folder
- **Backend README**: `backend/core/README.md`
- **Frontend README**: `frontend/console/README.md`
- **Environment Config**: `docs/ENVIRONMENT_CONFIG.md`
- **WorkOS Setup**: `docs/WORKOS_SETUP.md`

---

**Last Updated**: 2025-01-16
**Django Version**: 5.1
**React Version**: 19.2
**Node Version**: 24 LTS
**WorkOS SDK**: 5.32.0
