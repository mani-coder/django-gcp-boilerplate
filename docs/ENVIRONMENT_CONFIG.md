# Environment Configuration Guide

This document explains the layered environment configuration system used in this boilerplate.

## Overview

The project uses a **two-layer environment configuration** that separates safe defaults from sensitive credentials:

1. **`.env.dev`** - Committed to git with safe defaults
2. **`.env.dev.secrets`** - Gitignored file for your actual credentials (overrides `.env.dev`)

This approach provides several benefits:
- ✅ New developers can clone and run immediately (with placeholders)
- ✅ No risk of accidentally committing secrets
- ✅ Clear separation between config and secrets
- ✅ Easy to see what credentials are needed

## File Structure

```
backend/core/
├── .env.dev                    # Committed - safe defaults
├── .env.dev.secrets.example    # Committed - template
└── .env.dev.secrets            # Gitignored - your actual secrets
```

## How It Works

### 1. Base Configuration (`.env.dev`)

This file is **committed to the repository** and contains:
- Safe default values for local development
- Placeholder values for sensitive credentials
- Documentation on what each variable does

**Example:**
```bash
# Safe defaults - works out of the box
POSTGRES_HOST=localhost
POSTGRES_DB=django_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Placeholders - override in .env.dev.secrets
WORKOS_API_KEY=sk_test_placeholder_add_real_key_to_env_secrets
WORKOS_CLIENT_ID=client_placeholder_add_real_id_to_env_secrets
```

### 2. Secret Overrides (`.env.dev.secrets`)

This file is **gitignored** and contains your actual credentials:

```bash
# Your actual secrets
WORKOS_API_KEY=sk_test_abc123realkey456
WORKOS_CLIENT_ID=client_xyz789realid012
SECRET_KEY=actual-django-secret-key-here
```

### 3. Loading Order

The `settings.py` loads environment variables in this order:

```python
# 1. Load base configuration (.env.dev)
load_dotenv(".env.dev", override=False)

# 2. Load secrets override (.env.dev.secrets) - overrides base
if DEBUG and os.path.exists(".env.dev.secrets"):
    load_dotenv(".env.dev.secrets", override=True)
```

Variables in `.env.dev.secrets` **override** those in `.env.dev`.

## Quick Start

### For New Developers

1. Clone the repository
2. Create your secrets file:
   ```bash
   cd backend/core
   cp .env.dev.secrets.example .env.dev.secrets
   ```
3. Edit `.env.dev.secrets` with your actual credentials
4. Run the app - it works!

### What to Put in `.env.dev.secrets`

Only override the variables you actually need. Common ones:

**Required for authentication:**
```bash
WORKOS_API_KEY=sk_test_your_key
WORKOS_CLIENT_ID=client_your_id
```

**Required for security:**
```bash
SECRET_KEY=generate-a-secure-random-key
```

**Optional (only if different from defaults):**
```bash
GCP_PROJECT_ID=my-actual-project
POSTGRES_PASSWORD=my_custom_password
```

## Best Practices

### ✅ DO

- Commit `.env.dev` with safe defaults
- Put all real credentials in `.env.dev.secrets`
- Use placeholder values in `.env.dev` that clearly indicate they need to be replaced
- Document what each variable does in `.env.dev`
- Keep `.env.dev.secrets` minimal (only override what you need)

### ❌ DON'T

- Don't put real API keys in `.env.dev`
- Don't commit `.env.dev.secrets`
- Don't remove `.env.*.secrets` from `.gitignore`
- Don't duplicate all variables in `.env.dev.secrets` (only override what you need)

## Production Configuration

For production deployments to GCP:

1. Use `.env.prod` for production-specific settings
2. Store secrets in **GCP Secret Manager**
3. Reference secrets in Cloud Run environment variables

## Troubleshooting

### "I don't see my secrets being loaded"

Check that:
1. The file is named exactly `.env.dev.secrets` (note the `.secrets` suffix)
2. The file is in `backend/core/` directory
3. You're running in development mode (`ENV=dev`)
4. You see the log message: `Loaded secret overrides from .env.dev.secrets`

### "My values aren't being overridden"

Make sure:
1. Your `.env.dev.secrets` file exists
2. The variable names match exactly (case-sensitive)
3. There are no spaces around the `=` sign
4. The file is being loaded (check startup logs)

### "Should I commit my changes to `.env.dev`?"

**Yes!** If you're adding new configuration options that everyone needs, add them to `.env.dev` with safe default or placeholder values. Just never put real secrets there.

### "What if I need different database credentials?"

Override them in `.env.dev.secrets`:

```bash
POSTGRES_HOST=my-custom-host
POSTGRES_PASSWORD=my-secure-password
```

## Migration from Old Setup

If you're migrating from the old `.env.example` approach:

**Old way (❌):**
```bash
cp .env.example .env.dev
# Edit .env.dev with all your secrets
```

**New way (✅):**
```bash
# .env.dev already exists in the repo
cp .env.dev.secrets.example .env.dev.secrets
# Edit .env.dev.secrets with ONLY your secrets
```

Benefits:
- No risk of committing secrets by mistake
- Faster onboarding for new developers
- Clear distinction between config and secrets
- Easy to see what credentials are actually needed

## Environment Variables Reference

See `.env.dev` for the complete list of available environment variables and their default values.

For a template of what to put in your secrets file, see `.env.dev.secrets.example`.

## Related Documentation

- [WorkOS Setup](WORKOS_SETUP.md) - How to get WorkOS credentials
- [GCP Setup](GCP_SETUP.md) - How to configure GCP
- [Deployment](DEPLOYMENT.md) - Production deployment guide
