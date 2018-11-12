"""User management utilities for local user management."""

import secrets
from werkzeug.security import check_password_hash, generate_password_hash

from yeti.core.model.user import User

def create_user(email, password=None):
    user = User(email=email)
    set_password(user, password)
    return user.save()

def authenticate_user(email, password):
    user = User.find(email=email)
    if not user:
        return None
    if check_password_hash(user.password, password):
        return user
    return None

def set_password(user, password=None):
    if not password:
        password = secrets.token_hex(16)
    user.password = generate_password_hash(password, method='pbkdf2:sha256:100000')
    return password
