# Contributing to Django-GCP Boilerplate

Thank you for your interest in contributing! This document provides guidelines and workflows for contributing to this project.

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 24 LTS (see `.nvmrc`)
- PostgreSQL 16
- Git
- Google Cloud SDK (for deployment features)
- WorkOS account (for auth development)

### Initial Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/django-gcp-boilerplate.git
   cd django-gcp-boilerplate
   ```

2. **Set up backend**
   ```bash
   cd backend/core
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt -r dev-requirements.txt

   # Configure environment
   cp .env.dev.secrets.example .env.dev.secrets
   # Edit .env.dev.secrets with your credentials

   # Setup database
   createdb django_db
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Set up frontend**
   ```bash
   cd frontend/console
   nvm use  # Uses Node 24 from .nvmrc
   npm install

   # Copy environment file
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Verify setup**
   ```bash
   # Terminal 1: Backend
   cd backend/core
   python manage.py runserver

   # Terminal 2: Frontend
   cd frontend/console
   npm run dev

   # Visit http://localhost:3000 and test login
   ```

## Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards (see below)
   - Write tests for new features
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Backend tests
   cd backend/core
   python manage.py test

   # Frontend linting
   cd frontend/console
   npm run lint
   npm run format
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

   **Commit Message Format**:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding or updating tests
   - `chore:` - Maintenance tasks

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## Coding Standards

### Backend (Python/Django)

**Style Guide**: PEP 8

**Import Order**:
```python
# Standard Library Imports
import os
from typing import Optional

# Third Party Library Imports
from pydantic import BaseModel
from workos import WorkOSClient

# Django Imports
from django.conf import settings
from django.contrib.auth import login

# App Imports (same app)
from ..models import User

# App Imports (other apps)
from accounts.models import User
```

**Type Hints**:
```python
def authenticate(code: str) -> WorkOSUser:
    """Authenticate user with WorkOS code."""
    # ...
```

**Settings Access**:
```python
# ✅ Correct
from django.conf import settings
api_key = settings.WORKOS_API_KEY

# ❌ Wrong
import os
api_key = os.environ.get("WORKOS_API_KEY")
```

**Docstrings**:
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input provided
    """
    pass
```

### Frontend (TypeScript/React)

**Style Guide**: Enforced by ESLint and Prettier

**Formatting**:
```bash
# Format code before committing
npm run format

# Fix linting issues
npm run lint:fix
```

**Imports**:
```typescript
// React imports first
import { useState, useEffect } from 'react'

// Third-party imports
import { useNavigate } from 'react-router-dom'
import { useMutation } from 'urql'

// Local imports with @ alias
import { setAuthToken } from '@/lib/auth'
import { LOGIN_MUTATION } from '@/graphql/mutations'
```

**Component Structure**:
```typescript
import { useEffect, useState } from 'react'

interface Props {
  userId: string
}

export function MyComponent({ userId }: Props) {
  const [data, setData] = useState<string | null>(null)

  useEffect(() => {
    // Effect logic
  }, [userId])

  return <div>{data}</div>
}
```

**File Naming**:
- Components: `PascalCase.tsx` (e.g., `AuthCallback.tsx`)
- Utilities: `camelCase.ts` (e.g., `graphql-client.ts`)
- Pages: `PascalCase.tsx` in `pages/` directory

## GraphQL Development

### Adding a Mutation

1. **Backend**: Create mutation in `backend/core/accounts/gql/mutations/`
   ```python
   class MyMutation(graphene.Mutation):
       class Arguments:
           input = graphene.String(required=True)

       result = graphene.String()

       def mutate(self, info, input):
           return MyMutation(result="success")
   ```

2. **Register** in `backend/core/accounts/gql/mutations/__init__.py`

3. **Frontend**: Add to `frontend/console/src/graphql/mutations.ts`
   ```typescript
   export const MY_MUTATION = gql`
     mutation MyMutation($input: String!) {
       myMutation(input: $input) {
         result
       }
     }
   `
   ```

4. **Generate Types**:
   ```bash
   cd frontend/console
   npm run codegen
   ```

### Adding a Query

Follow similar process but in `queries/` directory and `queries.ts`.

## Testing

### Backend Tests

```bash
cd backend/core

# Run all tests
python manage.py test

# Run specific app
python manage.py test accounts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

**Writing Tests**:
```python
from django.test import TestCase
from accounts.models import User

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            email="test@example.com",
            workos_user_id="test_id"
        )
        self.assertEqual(user.email, "test@example.com")
```

### Frontend Tests

(To be added when test framework is set up)

## Documentation

### When to Update Docs

- Adding new features → Update relevant README
- Changing environment variables → Update `docs/ENVIRONMENT_CONFIG.md`
- Modifying GraphQL schema → Regenerate types
- Adding dependencies → Update relevant README

### Documentation Files

- `README.md` - Main project overview
- `backend/core/README.md` - Backend setup and development
- `frontend/console/README.md` - Frontend setup and development
- `CLAUDE.md` - AI-assisted development guide
- `docs/` - Detailed guides (WorkOS, GCP, etc.)

## Pull Request Process

1. **Before Submitting**:
   - ✅ All tests pass
   - ✅ Code is formatted (backend: PEP 8, frontend: Prettier)
   - ✅ No console errors or warnings
   - ✅ Documentation updated
   - ✅ GraphQL types regenerated (if schema changed)

2. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Backend tests pass
   - [ ] Frontend builds without errors
   - [ ] Manually tested locally

   ## Screenshots (if applicable)
   Add screenshots for UI changes
   ```

3. **Review Process**:
   - At least 1 approval required
   - All CI checks must pass
   - Address reviewer comments

4. **Merging**:
   - Squash and merge into `develop`
   - Delete feature branch after merge

## Common Development Tasks

### Adding Environment Variables

1. **Backend**:
   - Add to `backend/core/.env.dev` with safe default
   - Add to `backend/core/.env.dev.secrets.example` if secret
   - Reference in `backend/core/app/settings.py`
   - Update `docs/ENVIRONMENT_CONFIG.md`

2. **Frontend**:
   - Add to `frontend/console/.env.example` with `VITE_` prefix
   - Update `frontend/console/README.md`

### Adding Dependencies

**Backend**:
```bash
pip install package-name
pip freeze | grep package-name >> requirements.txt
```

**Frontend**:
```bash
npm install package-name
# package.json is automatically updated
```

### Database Migrations

```bash
# Create migration
python manage.py makemigrations

# Review migration file
cat accounts/migrations/000X_*.py

# Apply migration
python manage.py migrate

# Rollback if needed
python manage.py migrate accounts 000X_previous
```

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security**: Email security@yourproject.com
- **Documentation**: Check `docs/` folder first

## Code Review Guidelines

### For Reviewers

- Check code follows style guidelines
- Verify tests are included
- Ensure documentation is updated
- Test changes locally if significant
- Be constructive and respectful

### For Contributors

- Respond to feedback promptly
- Don't take criticism personally
- Ask questions if unclear
- Update PR based on feedback

## Release Process

(To be defined when project reaches v1.0)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
