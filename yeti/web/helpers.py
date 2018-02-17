import functools

from flask import jsonify

from yeti.core.errors import GenericYetiError
from yeti.core.model.database import YetiObject

def as_json(func):
    """Attempts to jsonify YetiObjects and lists of YetiObjects."""
    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, tuple):
            response, code = result
            if isinstance(response, GenericYetiError):
                return jsonify({response.type: response.message}), code
        if isinstance(result, list):
            return jsonify([item.dump() for item in result])
        if isinstance(result, YetiObject):
            return jsonify(result.dump())
        return result
    return inner

def get_object_or_404(klass, key):
    """Fetch an object form the YetiObject klass, return 404 if nonexistent."""
    obj = klass.get(key)
    if not obj:
        return '', 404
    return obj
