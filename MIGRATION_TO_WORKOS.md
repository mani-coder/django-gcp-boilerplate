# Migration from Firebase Auth to WorkOS

This document outlines the changes made to migrate from Firebase Authentication to WorkOS.

## Summary of Changes

This boilerplate has been updated to use **WorkOS** instead of Firebase for authentication. WorkOS offers:
- Free tier for up to 1 million Monthly Active Users (MAU)
- Enterprise SSO support (SAML, OAuth, OpenID Connect)
- Built-in Admin Portal for enterprise customers
- Social login providers (Google, Microsoft, GitHub, etc.)
- Magic link authentication

## Files Changed

### New Files
- `backend/core/accounts/workos_auth.py` - WorkOS authentication module
- `backend/core/accounts/migrations/0002_rename_firebase_to_workos.py` - Database migration
- `docs/WORKOS_SETUP.md` - Complete WorkOS setup guide
- `MIGRATION_TO_WORKOS.md` - This file

### Modified Files
- `backend/core/requirements.txt` - Removed `firebase_admin`, added `workos`
- `backend/core/accounts/models.py` - Renamed `firebase_uid` to `workos_user_id`
- `backend/core/accounts/gql/mutations/login.py` - Updated to use WorkOS authentication
- `backend/core/.env.example` - Updated environment variables for WorkOS
- `README.md` - Updated documentation to reflect WorkOS

### Deleted Files
- `backend/core/accounts/firebase.py` - Firebase authentication module (replaced)
- `docs/FIREBASE_SETUP.md` - Firebase setup guide (replaced with WORKOS_SETUP.md)

## Migration Steps for Existing Projects

If you have an existing project using the old Firebase-based boilerplate, follow these steps:

### 1. Update Dependencies

```bash
pip install workos==5.4.0
pip uninstall firebase-admin
```

### 2. Update Environment Variables

The project now uses a layered environment setup:
- `.env.dev` - Committed with safe defaults
- `.env.dev.secrets` - Gitignored for your actual credentials

Create your secrets file:

```bash
cd backend/core
cp .env.dev.secrets.example .env.dev.secrets
```

Add your WorkOS credentials to `.env.dev.secrets`:

```bash
WORKOS_API_KEY=sk_test_your_actual_api_key
WORKOS_CLIENT_ID=client_your_actual_client_id
```

**Old Firebase variables (remove from any custom env files):**
```bash
FIREBASE_AUTH_CREDS_HASH=...
```

### 3. Run Database Migration

```bash
python manage.py migrate
```

This will rename the `firebase_uid` field to `workos_user_id` in the database.

### 4. Update Existing Users (if applicable)

If you have existing users in your database, you'll need to handle the migration:

**Option A: Fresh Start**
If you're okay with users re-authenticating, no action needed. They'll be created as new users when they log in via WorkOS.

**Option B: Migrate User Data**
If you need to preserve user data, you'll need to manually map Firebase UIDs to WorkOS user IDs. This is beyond the scope of this boilerplate but can be done with a custom Django management command.

### 5. Update Frontend Code

Update your frontend authentication flow:

**Old (Firebase):**
```javascript
// Firebase initialization and ID token
const idToken = await firebase.auth().currentUser.getIdToken();

// Login mutation
mutation {
  login(firebaseToken: $idToken) { ... }
}
```

**New (WorkOS):**
```javascript
// Redirect to WorkOS
window.location.href = workosAuthUrl;

// Handle callback with authorization code
mutation {
  login(code: $code) { ... }
}
```

See `docs/WORKOS_SETUP.md` for complete frontend integration examples.

### 6. Update GCP Deployment

If deploying to GCP:

1. Update environment variables in Cloud Run
2. Remove Firebase credentials from Secret Manager
3. Add WorkOS credentials to Secret Manager
4. Update `deploy/core.yaml` if it references Firebase

## Benefits of WorkOS

### Free Tier
- **1 million MAU** vs Firebase's pricing model
- Better for growing applications

### Enterprise Features
- **SSO Support**: SAML, OAuth 2.0, OpenID Connect out of the box
- **Admin Portal**: Self-service for enterprise customers
- **Audit Logs**: Track authentication events

### Developer Experience
- Simpler integration (no need for Firebase SDK in frontend)
- Better documentation
- Modern OAuth 2.0 flow
- Support for multiple authentication methods

### Production Ready
- Built for B2B SaaS applications
- Compliance-ready (SOC 2, GDPR)
- Enterprise support available

## GraphQL API Changes

### Login Mutation

**Before:**
```graphql
mutation {
  login(firebaseToken: "firebase_id_token") {
    responseCode
    token
    user {
      id
      email
    }
  }
}
```

**After:**
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

### Response Codes

- `INVALID_TOKEN` → `INVALID_CODE`
- `LOGIN_SUCCESS` remains the same

## Testing

1. Get WorkOS credentials from https://dashboard.workos.com
2. Set up environment variables
3. Run migrations
4. Test the login flow through GraphiQL

## Rollback Plan

If you need to rollback to Firebase:

1. Checkout the previous commit before this migration
2. Restore Firebase credentials
3. Run database migrations to revert the field rename
4. Redeploy

## Support

- WorkOS Documentation: https://workos.com/docs
- WorkOS Support: https://workos.com/support
- Boilerplate Issues: GitHub Issues

## Next Steps

1. Review `docs/WORKOS_SETUP.md` for detailed setup instructions
2. Configure your WorkOS dashboard at https://dashboard.workos.com
3. Test authentication flow in development
4. Deploy to production with live credentials
