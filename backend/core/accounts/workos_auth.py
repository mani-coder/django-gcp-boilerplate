# Standard Library Imports
from functools import wraps

# Third Party Library Imports
from pydantic import BaseModel
from workos import WorkOSClient

# Django Imports
from django.conf import settings


_client = None


def get_workos_client():
    """Get or create WorkOS client instance."""
    global _client
    if not _client:
        if not settings.WORKOS_API_KEY:
            raise ValueError("WORKOS_API_KEY setting is required")
        _client = WorkOSClient(api_key=settings.WORKOS_API_KEY)
    return _client


class WorkOSUser(BaseModel):
    """WorkOS user representation."""
    id: str
    email: str
    first_name: str = ""
    last_name: str = ""


def workos_call(func):
    """Decorator to ensure WorkOS client is initialized."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        get_workos_client()
        return func(*args, **kwargs)
    return wrapper


@workos_call
def authenticate(code: str) -> WorkOSUser:
    """
    Authenticate user with WorkOS authorization code.

    Args:
        code: Authorization code from WorkOS OAuth flow

    Returns:
        WorkOSUser object with user information

    Raises:
        Exception: If authentication fails
    """
    client = get_workos_client()

    if not settings.WORKOS_CLIENT_ID:
        raise ValueError("WORKOS_CLIENT_ID setting is required")

    # Exchange authorization code for access token and user profile
    profile_and_token = client.user_management.authenticate_with_code(
        code=code,
        client_id=settings.WORKOS_CLIENT_ID,
    )

    user_data = profile_and_token.user

    return WorkOSUser(
        id=user_data.id,
        email=user_data.email,
        first_name=user_data.first_name or "",
        last_name=user_data.last_name or "",
    )


@workos_call
def verify_session(session_id: str) -> WorkOSUser:
    """
    Verify a WorkOS session and return user information.

    Args:
        session_id: WorkOS session ID to verify

    Returns:
        WorkOSUser object with user information

    Raises:
        Exception: If session is invalid or expired
    """
    client = get_workos_client()

    # Authenticate the session
    session = client.user_management.authenticate_with_session(
        session_id=session_id,
    )

    user_data = session.user

    return WorkOSUser(
        id=user_data.id,
        email=user_data.email,
        first_name=user_data.first_name or "",
        last_name=user_data.last_name or "",
    )


@workos_call
def get_authorization_url(
    redirect_uri: str = None,
    state: str = None,
    provider: str = None,
) -> str:
    """
    Get WorkOS authorization URL for OAuth flow.

    Args:
        redirect_uri: URL to redirect to after authentication (defaults to WORKOS_REDIRECT_URI setting)
        state: Optional state parameter for CSRF protection
        provider: Optional provider to use (e.g., 'GoogleOAuth', 'MicrosoftOAuth')

    Returns:
        Authorization URL string
    """
    client = get_workos_client()

    if not settings.WORKOS_CLIENT_ID:
        raise ValueError("WORKOS_CLIENT_ID setting is required")

    if not redirect_uri:
        redirect_uri = settings.WORKOS_REDIRECT_URI

    params = {
        "client_id": settings.WORKOS_CLIENT_ID,
        "redirect_uri": redirect_uri,
    }

    if state:
        params["state"] = state

    if provider:
        params["provider"] = provider

    return client.user_management.get_authorization_url(**params)
