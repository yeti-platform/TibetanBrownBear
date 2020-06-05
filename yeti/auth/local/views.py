"""API resources for interacting with Users."""
from datetime import datetime, timedelta

import jwt
from flask import request
from flask_classful import FlaskView, route
from marshmallow import fields
from webargs.flaskparser import parser

from yeti.auth.local import user_management
from yeti.common.config import yeti_config
from yeti.core.errors import RuntimeException
from yeti.core.model.user import User

from yeti.web.helpers import as_json, auth_required
from yeti.web.api.generic import GenericResource


class UserResource(GenericResource):  # FlaskView
    """Class describing resources to manipulate User objects."""

    route_base = '/users/'
    resource_object = User

    searchargs = {
        'email': fields.Str(required=True),
    }

    loginargs = {
        'email': fields.Str(required=True),
        'password': fields.Str(required=True)
    }

    @as_json
    @route('/protected/', methods=['GET'])
    @auth_required
    def protected(self):
        return {'msg': 'You\'re in!'}

    @as_json
    @route('/login/', methods=['POST'])
    def login(self):
        """Authenticate a user and return a user object if sucessful."""
        data = parser.parse(self.loginargs, request)
        email = data['email']
        password = data['password']

        try:
            user = user_management.authenticate_user(email, password)
        except RuntimeException as exception:
            return exception, 400
        if not user:
            return {'error': f'Invalid credentials for {email}.'}, 401

        token = jwt.encode({
            'sub': user.email,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30),
        }, yeti_config.core.secret_key)

        return {'token': token.decode('UTF-8'), 'authenticated': True}
