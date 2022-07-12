"""User management utilities for local user management."""

import secrets
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from yeti.core.model.user import User


def create_user(email):
    """Creates a user in the database.

    Args:
      email: The user's email address.

    Returns:
      The new User object.
    """
    user = User(email=email)
    user.api_key = secrets.token_hex(32)
    user.last_password_change = datetime.utcnow()
    return user.save()

def authenticate_user(email):
    """Authenticates a user against the information in the database.

    Args:
      email: The user's email address.
      password: The user's cleartext password.

    Returns:
      A User obejct if authentication is successful, None otherwise.
    """
    user = User.find(email=email)
    if not user:
        return create_user(email)
    return user
