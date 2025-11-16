# WorkOS Setup Guide

This guide will walk you through setting up WorkOS authentication for your Django-GCP boilerplate.

## Why WorkOS?

WorkOS provides enterprise-ready authentication with:
- **Free tier**: Up to 1 million Monthly Active Users (MAU)
- **SSO Support**: SAML, OAuth 2.0, OpenID Connect
- **Social Login**: Google, Microsoft, GitHub, and more
- **Magic Links**: Passwordless authentication
- **User Management**: Built-in user directory
- **Admin Portal**: Self-service for enterprise customers
- **Audit Logs**: Track authentication events

## Prerequisites

- A WorkOS account (sign up at https://workos.com)
- Your Django application running locally or deployed

## Step 1: Create a WorkOS Account

1. Go to https://workos.com and click "Get Started"
2. Sign up for a free account
3. Verify your email address

## Step 2: Set Up Your Environment

1. Log in to the [WorkOS Dashboard](https://dashboard.workos.com/)
2. Create a new environment (Development/Production)
3. Note your **API Key** and **Client ID** from the dashboard

## Step 3: Configure Redirect URI

1. In the WorkOS Dashboard, navigate to **Configuration** > **Redirects**
2. Add your redirect URI:
   - For local development: `http://localhost:8000/auth/callback`
   - For production: `https://your-domain.com/auth/callback`

## Step 4: Enable Authentication Methods

1. In the WorkOS Dashboard, go to **Authentication** > **Methods**
2. Enable the authentication methods you want to support:
   - **Google OAuth**: Social login with Google
   - **Microsoft OAuth**: Social login with Microsoft
   - **GitHub OAuth**: Social login with GitHub
   - **Magic Link**: Passwordless email authentication
   - **Email/Password**: Traditional authentication
   - **SAML SSO**: Enterprise single sign-on (for enterprise customers)

## Step 5: Configure Environment Variables

Create `.env.dev.secrets` from the template:

```bash
cd backend/core
cp .env.dev.secrets.example .env.dev.secrets
```

Edit `.env.dev.secrets` and add your WorkOS credentials:

```bash
# WorkOS Configuration
WORKOS_API_KEY=sk_test_your_actual_api_key_here
WORKOS_CLIENT_ID=client_your_actual_client_id_here
```

**Important**:
- The base `.env.dev` is committed to the repository with safe placeholder values
- Your actual credentials go in `.env.dev.secrets` which is gitignored
- `.env.dev.secrets` overrides values from `.env.dev`

For production, add these to your `.env.prod` or GCP Secret Manager:

```bash
WORKOS_API_KEY=sk_live_your_api_key_here
WORKOS_CLIENT_ID=client_your_client_id_here
WORKOS_REDIRECT_URI=https://your-domain.com/auth/callback
```

## Step 6: Install Dependencies

The WorkOS Python SDK is already included in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Step 7: Run Database Migrations

Run the migration to update the user model:

```bash
python manage.py migrate
```

## Step 8: Test Authentication

### Using GraphQL

1. Start your development server:
   ```bash
   python manage.py runserver
   ```

2. Open GraphiQL at `http://localhost:8000/graphiql/`

3. Get an authorization URL first (you can create a helper mutation or use the WorkOS dashboard)

4. Complete the OAuth flow and get an authorization code

5. Use the login mutation:
   ```graphql
   mutation {
     login(code: "your_authorization_code") {
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

### Integration Flow

Here's how the authentication flow works:

1. **Frontend**: Redirect user to WorkOS authorization URL
2. **User**: Authenticates with chosen provider (Google, Microsoft, etc.)
3. **WorkOS**: Redirects back to your app with an authorization code
4. **Backend**: Exchange code for user profile (handled by the login mutation)
5. **Backend**: Create or update user in database
6. **Backend**: Return JWT token to frontend
7. **Frontend**: Store token and use for subsequent API requests

## Step 9: Frontend Integration Example

Here's a simple example of how to integrate WorkOS in your frontend:

```javascript
// Get the authorization URL
const getAuthUrl = async (provider = 'GoogleOAuth') => {
  const params = new URLSearchParams({
    client_id: 'YOUR_CLIENT_ID',
    redirect_uri: 'http://localhost:8000/auth/callback',
    response_type: 'code',
    provider: provider, // GoogleOAuth, MicrosoftOAuth, GitHubOAuth, etc.
  });

  return `https://api.workos.com/user_management/authorize?${params}`;
};

// Redirect user to WorkOS
const login = async () => {
  const authUrl = await getAuthUrl('GoogleOAuth');
  window.location.href = authUrl;
};

// Handle callback (in your /auth/callback route)
const handleCallback = async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');

  // Send code to your GraphQL API
  const response = await fetch('/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: `
        mutation Login($code: String!) {
          login(code: $code) {
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
      `,
      variables: { code }
    })
  });

  const data = await response.json();

  if (data.data.login.responseCode === 'LOGIN_SUCCESS') {
    // Store token
    localStorage.setItem('token', data.data.login.token);
    // Redirect to dashboard
    window.location.href = '/dashboard';
  }
};
```

## Advanced Configuration

### Using Multiple Providers

You can enable multiple authentication providers and let users choose:

```python
# In your view or mutation
from accounts.workos_auth import get_authorization_url

# Google OAuth
google_url = get_authorization_url(
    redirect_uri="http://localhost:8000/auth/callback",
    provider="GoogleOAuth"
)

# Microsoft OAuth
microsoft_url = get_authorization_url(
    redirect_uri="http://localhost:8000/auth/callback",
    provider="MicrosoftOAuth"
)

# Generic (shows all enabled providers)
auth_url = get_authorization_url(
    redirect_uri="http://localhost:8000/auth/callback"
)
```

### Session-based Authentication

WorkOS also supports session-based authentication. See the `verify_session` function in `accounts/workos_auth.py`.

### Admin Portal for Enterprise SSO

WorkOS provides an Admin Portal for enterprise customers to configure their own SSO:

1. Enable the Admin Portal in your WorkOS Dashboard
2. Send the portal link to your enterprise customers
3. They can configure SAML/OIDC on their own

## Troubleshooting

### Invalid Client ID Error

- Make sure `WORKOS_CLIENT_ID` in your `.env` file matches the Client ID in the WorkOS Dashboard
- Check that you're using the correct environment (development vs production)

### Redirect URI Mismatch

- Ensure the redirect URI in your WorkOS Dashboard exactly matches the one in your code
- Include the protocol (`http://` or `https://`)
- Match trailing slashes exactly

### User Not Created

- Check your application logs for errors
- Ensure database migrations have been run
- Verify that the WorkOS user data includes an email address

## Production Checklist

Before going to production:

- [ ] Switch from test API key (`sk_test_*`) to live API key (`sk_live_*`)
- [ ] Update `WORKOS_REDIRECT_URI` to your production domain
- [ ] Add production redirect URI to WorkOS Dashboard
- [ ] Enable only the authentication methods you need
- [ ] Set up proper error logging and monitoring
- [ ] Configure GCP Secret Manager for sensitive credentials
- [ ] Test the full authentication flow in production

## Additional Resources

- [WorkOS Documentation](https://workos.com/docs)
- [WorkOS Python SDK](https://github.com/workos/workos-python)
- [WorkOS User Management Guide](https://workos.com/docs/user-management)
- [WorkOS Admin Portal](https://workos.com/docs/admin-portal)

## Support

For issues with WorkOS:
- Check the [WorkOS Documentation](https://workos.com/docs)
- Contact [WorkOS Support](https://workos.com/support)

For issues with this boilerplate:
- Open an issue on GitHub
- Check the [Customization Guide](CUSTOMIZATION.md)
