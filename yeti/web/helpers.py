import functools

from flask import jsonify
import json

from yeti.core.errors import GenericYetiError
from yeti.core.model.database import YetiObject

def _as_json(result):
    if isinstance(result, tuple):
        response, code = result
        if isinstance(response, GenericYetiError):
            # necessary since jsonify seems to be broken when sorting
            error_msg = json.dumps({response.type: response.message})
            return jsonify(error_msg), code
        return jsonify(response), code
    if isinstance(result, list):
        return jsonify([item.dump() for item in result])
    if isinstance(result, YetiObject):
        return jsonify(result.dump())
    return jsonify(result)

def as_json(func):
    """Attempts to jsonify YetiObjects and lists of YetiObjects."""
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return _as_json(func(*args, **kwargs))
    return inner

def get_object_or_404(klass, key):
    """Fetch an object form the YetiObject klass, return 404 if nonexistent."""
    obj = klass.get(key)
    if not obj:
        return '', 404
    return obj
