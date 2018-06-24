import functools

from flask import jsonify

from yeti.core.errors import GenericYetiError
from yeti.core.model.database import YetiObject

def _as_json(result): # pylint: disable=too-many-return-statements
    if isinstance(result, tuple):
        response, code = result
        if isinstance(response, GenericYetiError):
            return jsonify({response.type: response.message}), code
        return jsonify(response), code
    if isinstance(result, list):
        if not result:
            return jsonify([])
        if isinstance(result[0], YetiObject):
            return jsonify([item.dump(destination='web') for item in result])
        if isinstance(result[0], dict):
            return jsonify(result)
    if isinstance(result, YetiObject):
        return jsonify(result.dump(destination='web'))
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
