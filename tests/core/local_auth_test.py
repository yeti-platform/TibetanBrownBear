# pylint: disable=unused-argument
"""Tests for Yeti local user management"""
import pytest

from werkzeug.security import check_password_hash

from yeti.core.model.user import User
from yeti.auth.local import user_management


@pytest.mark.usefixtures('clean_db')
def test_create_user():
    """Tests that a user can be created."""
    user = user_management.create_user('user@email.com')
    assert user is not None
    assert user.password is not None

@pytest.mark.usefixtures('clean_db')
def test_new_user_manual_password():
    """Tests that a user can be created with a password."""
    user = user_management.create_user('user@email.com', password='toto')
    assert user_management.check_password_hash(user.password, 'toto')

@pytest.mark.usefixtures('clean_db')
def test_existing_user_auto_password(populate_users):
    """Tests that an existing user's password can be regenerated."""
    user = populate_users[0]
    password = user_management.set_password(user)
    user.save()
    assert len(password) == 32
    assert check_password_hash(user.password, password)

@pytest.mark.usefixtures('clean_db')
def test_existing_user_manual_password(populate_users):
    """Tests that a password can be set on an existing user."""
    user = populate_users[0]
    user_management.set_password(user, 'weakpassword')
    user.save()
    assert check_password_hash(user.password, 'weakpassword')

@pytest.mark.usefixtures('clean_db')
def test_filter_users(populate_users):
    """Tests that users are correctly populated and can be searched for."""
    users = User.filter({'email': 'user'})
    assert len(users) == 1
    users = User.filter({'email': 'admin'})
    assert len(users) == 1

@pytest.mark.usefixtures('clean_db')
def test_no_override_password():
    """Tests that updates to a user do not override their password."""
    user = User(email='password@email.com').save()
    user_management.set_password(user, 'password')
    user.save()
    user.email = 'secure@email.com'
    user.save()
    user = User.find(email='secure@email.com')
    assert user.email == 'secure@email.com'
    assert check_password_hash(user.password, 'password')

@pytest.mark.usefixtures('clean_db')
def test_authenticate_success():
    """Tests that a user can be authenticated with their password."""
    user = User(email='password@email.com').save()
    user_management.set_password(user, 'password')
    user.save()
    assert user_management.authenticate_user(
        'password@email.com', 'password') is not None

@pytest.mark.usefixtures('clean_db')
def test_authenticate_fail():
    """Tests that a user can be authenticated with their password."""
    user = User(email='password@email.com').save()
    user_management.set_password(user, 'password')
    user.save()
    assert user_management.authenticate_user(
        'password@email.com', '123456') is None
