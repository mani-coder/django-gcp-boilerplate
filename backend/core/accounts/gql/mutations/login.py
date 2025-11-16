# Standard Library Imports
import logging

# Third Party Library Imports
import graphene

# Django Imports
from django.contrib.auth import login
from graphql_jwt.shortcuts import get_token

# Same App Imports
from ...workos_auth import authenticate
from ..schema import User

# App Imports
from accounts.models import User as UserModel


logger = logging.getLogger(__name__)


class LoginUserResponseCode(graphene.Enum):
    # Authorization code is invalid.
    INVALID_CODE = 1

    # Login is successful.
    LOGIN_SUCCESS = 2


class Login(graphene.Mutation):
    """
    Perform user login with WorkOS.
    """

    response_code = graphene.NonNull(LoginUserResponseCode, description="Login response code.")
    user = graphene.Field(lambda: User, description="Logged in user at the end of this mutation")
    token = graphene.String(description="JWT access token")

    class Arguments(object):
        code = graphene.NonNull(graphene.String, description="WorkOS authorization code")

    def mutate(self, info, code):
        logger.info(f"Login attempt with code: {code[:10]}...")
        try:
            workos_user = authenticate(code)
            logger.info(f"WorkOS authentication successful for user: {workos_user.email}")

            if workos_user:
                user = UserModel.objects.filter(workos_user_id=workos_user.id).first()
                if not user:
                    # Create new user from WorkOS profile
                    user = UserModel(
                        email=workos_user.email,
                        workos_user_id=workos_user.id,
                        first_name=workos_user.first_name,
                        last_name=workos_user.last_name,
                    )
                    user.save()
                    logger.info(f"Created new user {user.id} for WorkOS user: {workos_user.id}")
                else:
                    # Update user info from WorkOS profile
                    user.first_name = workos_user.first_name
                    user.last_name = workos_user.last_name
                    user.save()
                    logger.info(f"Updated existing user {user.id}")

                login(info.context, user, backend="django.contrib.auth.backends.ModelBackend")

                return Login(response_code=LoginUserResponseCode.LOGIN_SUCCESS, user=user, token=get_token(user))
        except Exception as e:
            logger.error(f"WorkOS authentication failed: {str(e)}", exc_info=True)

        return Login(response_code=LoginUserResponseCode.INVALID_CODE)
