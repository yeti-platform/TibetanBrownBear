"""Populate Yeti's database with pre-defined vocabulary lists."""
import click

from yeti.auth.local import user_management
from yeti.core.model.user import User

# pylint: disable=line-too-long
@click.command()
@click.option('--password', prompt='Password', hide_input=True, confirmation_prompt=True, help='Take password from CLI', type=click.STRING)
@click.argument('user_email')
def add_user(user_email, password=None):
    user = User(email=user_email).save()
    user_management.set_password(user, password)
    user.save()
    print(f'User {user_email} created succesfully (ID: {user.id})')
