# Standard Library Imports
from datetime import datetime
from datetime import timedelta

# Third Party Library Imports
import jwt
from django.conf import settings

# App Imports
from accounts.models import User


def generate_login_access_token(user: User, expiry=datetime.now() + timedelta(days=30)) -> str:
    payload = {"user_id": user.id, "exp": expiry}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def verify_login_access_token(token) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        user = User.objects.get(id=user_id)
        return user
    except jwt.ExpiredSignatureError:
        return None
