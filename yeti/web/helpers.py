import base64
import functools
from datetime import datetime

import jwt
from flask import g, jsonify, request

from yeti.common.config import yeti_config
from yeti.core.errors import GenericYetiError
from yeti.core.model.database import YetiObject
from yeti.core.model.user import User

INVALID_TOKEN = {
    'message': 'Invalid or nonexistent token. Please get a new token.',
    'authenticated': False
}
EXPIRED_TOKEN = {
    'message': 'Expired token. Please log in again.',
    'authenticated': False
}

INVALID_API_KEY = {
    'message': 'Invalid API key.',
    'authenticated': False
}

def auth_required(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', None)
        api_key = request.headers.get('X-Yeti-API', None)
        user = None

        if api_key:
            user = User.find(api_key=api_key)
            if not user:
                return INVALID_API_KEY, 401

        if auth_headers:
            try:
                token = auth_headers.split()[1]
                data = jwt.decode(token, yeti_config.core.secret_key)
                user = User.find(email=data['sub'])
                issued_at = datetime.utcfromtimestamp(data['iat'])
                last_pwd_reset = user.last_password_change.replace(
                    microsecond=0)
                if issued_at < last_pwd_reset:
                    return EXPIRED_TOKEN, 401
            except jwt.ExpiredSignatureError:
                return EXPIRED_TOKEN, 401
            except jwt.InvalidTokenError:
                pass

        if not user:
            return INVALID_TOKEN, 401
        g.user = user
        return f(*args, **kwargs)
    return inner


def _as_json(result): # pylint: disable=too-many-return-statements
    if isinstance(result, list):
        if not result:
            return []
        return [_as_json(item) for item in result]
    if isinstance(result, dict):
        return {key: _as_json(value) for key, value in result.items()}
    if isinstance(result, YetiObject):
        return result.dump(destination='web')
    return result

def as_json(func):
    """Attempts to jsonify YetiObjects and lists of YetiObjects."""
    @functools.wraps(func)
    def inner(*args, **kwargs):
        json_response = _as_json(func(*args, **kwargs))
        if isinstance(json_response, tuple):
            response, code = json_response
            if isinstance(response, GenericYetiError):
                return jsonify({response.type: response.message}), code
            return jsonify(response), code
        return jsonify(json_response)
    return inner

def get_object_or_404(klass, key):
    """Fetch an object form the YetiObject klass, return 404 if nonexistent."""
    obj = klass.get(key)
    if not obj:
        return '', 404
    return obj

def decode_object(object_dict):
    if object_dict['encoding'] == 'b64':
        return base64.b64decode(object_dict['data'])
    if object_dict['encoding'] == 'utf-8':
        return bytes(object_dict['data'], 'utf-8')
    return object_dict['data']
