"""API resources for interacting with Users."""
from datetime import datetime, timedelta

import jwt
from flask import request, g, session
from flask_classful import FlaskView, route
from marshmallow import fields
from webargs.flaskparser import parser
import requests
import json

from oauthlib.oauth2 import WebApplicationClient

from yeti.auth.oidc import user_management
from yeti.common.config import yeti_config
from yeti.core.errors import RuntimeException
from yeti.core.model.user import User
from yeti.web.api.generic import GenericResource
from yeti.web.helpers import as_json, auth_required

client = WebApplicationClient(yeti_config.oidc.client_id)


class UserResource(FlaskView):
    """Class describing resources to manipulate User objects."""

    route_base = '/auth/'
    resource_object = User

    @as_json
    @route('/me', methods=['GET'])
    @auth_required
    def protected(self):
        return {'authenticated': True, 'user': g.user.email}

    @as_json
    @route('/login/', methods=['POST'])
    def login(self):
        """Setup request and send OIDC redirect URL."""
        if 'user' in g:
            return {'redirect': '/', 'authenticated': True}

        provider_cfg = get_google_provider_cfg()
        authorization_endpoint = provider_cfg['authorization_endpoint']

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "callback",
            scope=['openid', 'email', 'profile']
        )

        return {'redirect': request_uri}

    @as_json
    @route('/login/callback', methods=['GET', 'POST'])
    def login_callback(self):
        """Authenticate a user and return a user object if sucessful."""
        code = request.args.get('code')

        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        # Send request for token with the  code received in the callback
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(yeti_config.oidc.client_id, yeti_config.oidc.client_secret),
        )

        client.parse_request_body_response(json.dumps(token_response.json()))
        # Our client can now get information on the user

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        # userinfo_response.json().get("email_verified")
        # unique_id = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        # picture = userinfo_response.json()["picture"]
        # users_name = userinfo_response.json()["given_name"]

        user = user_management.authenticate_user(user_email)

        token = jwt.encode({
            'sub': user.email,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=30),
        }, yeti_config.core.secret_key)

        session.clear()
        session['token'] = token.decode('utf-8')

        return {'authenticated': True, 'user': user.email}

    @as_json
    @route('/logout/', methods=['PUT'])
    @auth_required
    def logout(self):
        """Logout user."""
        session.clear()
        return {'authenticated': False}


def get_google_provider_cfg():
    discovery_url = yeti_config.oidc.google_discovery_url
    return requests.get(discovery_url).json()
