import functools

from flask import jsonify

def as_json(serializer):
    """Attempts to jsonify YetiObjects and lists of YetiObjects."""
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, list):
                return jsonify(serializer.dump_many(result))
            if isinstance(result, serializer):
                return jsonify(serializer.dump(result))
            return result
        return inner
    return wrapper


def get_object_or_404(klass, key):
    """Fetch an object form the YetiObject klass, return 404 if nonexistent."""
    obj = klass.get(key)
    if not obj:
        return "", 404
    return obj
