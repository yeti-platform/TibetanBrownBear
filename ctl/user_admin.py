"""Populate Yeti's database with pre-defined vocabulary lists."""
import click

from yeti.auth.local import user_management
from yeti.core.model.user import User
from yeti.core.errors import IntegrityError

# pylint: disable=line-too-long
@click.command()
@click.option('--password', prompt='Password', hide_input=True, confirmation_prompt=True, help='Take password from CLI', type=click.STRING)
@click.option('--admin', help='Give admin rights to this user', is_flag=True, default=False)
@click.argument('user_email')
def add_user(user_email, password=None, admin=False):
    try:
        user = User(email=user_email, admin=admin).save()
        user_management.set_password(user, password)
        user.save()
    except IntegrityError:  # user already exists, force reset password
        user = User.get_or_create(email=user_email)
        user_management.set_password(user, password)

    print(f'User {user_email} created succesfully (ID: {user.id})')
    print(f'Admin: {user.admin}')
    print(f'API key: {user.api_key}')

@click.command()
@click.option('--password', prompt='Password', hide_input=True, confirmation_prompt=True, help='Take password from CLI', type=click.STRING)
@click.argument('user_email')
def reset_password(user_email, password=None):
    user = User.find(email=user_email)
    if not user:
        print(f'No such user: {user_email}')
        exit(-1)
    user_management.set_password(user, password)
    user.save()
    print(f'Password for {user_email} reset succesfully.')
    print(f'Admin: {user.admin}')
    print(f'API key: {user.api_key}')
