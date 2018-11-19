"""User management utilities for local user management."""

import secrets
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from yeti.core.model.user import User


def create_user(email, password=None):
    """Creates a user in the database.

    Args:
      email: The user's email address.
      password: The user's cleartext password.

    Returns:
      The new User object.
    """
    user = User(email=email)
    set_password(user, password)
    return user.save()

def authenticate_user(email, password):
    """Authenticates a user against the information in the database.

    Args:
      email: The user's email address.
      password: The user's cleartext password.

    Returns:
      A User obejct if authentication is successful, None otherwise.
    """
    user = User.find(email=email)
    if not user:
        return None
    if check_password_hash(user.password, password):
        return user
    return None

def set_password(user, password=None):
    """Sets a user password and API keys.

    The API key is regenerated every time the password is set. The password
    is salted and hashed before being stored.

    Args:
      password: The password to set.

    Returns:
      The cleartext password associated with the user.
    """
    if not password:
        password = secrets.token_hex(16)
    user.password = generate_password_hash(
        password, method='pbkdf2:sha256:100000')
    user.api_key = secrets.token_hex(32)
    user.last_password_change = datetime.utcnow()
    return password
