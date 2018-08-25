"""API resources for interacting with Entities."""
from marshmallow import fields
from flask_classful import route
from flask import request
from stix2.exceptions import UnmodifiablePropertyError


from yeti.core.entities.entity import Entity
from .generic import GenericResource
from ..helpers import as_json, get_object_or_404
from yeti.core.errors import YetiSTIXError


class EntityResource(GenericResource):
    """Class describing resources to manipulate Entity objects."""

    route_base = '/entities/'
    resource_object = Entity

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }

    @as_json
    @route('/<id>/', methods=['PUT'])
    def put(self, id):  # pylint: disable=redefined-builtin
        """Updates a STIX SDO object.

        Args:
            id: The object's primary ID.

        Returns:
            A JSON representation of the requested object, or a 404 HTTP
            status code if the object cannot be found.
        """
        # Remove unupdatable fields (created, id, type) from the request JSON
        # Also remove the 'modified' field since we want STIX to change the
        # timestamp
        update_dict = request.get_json()
        update_dict.pop('created', None)
        update_dict.pop('id', None)
        update_dict.pop('type', None)
        update_dict.pop('modified', None)
        try:
            obj = get_object_or_404(self.resource_object, id)
            return obj.update(update_dict)
        except YetiSTIXError as err:
            return err, 400
