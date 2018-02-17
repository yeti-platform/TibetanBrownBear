"""API endpionts for Yeti."""

from flask import Blueprint

from .observable import ObservableResource
from .entity import EntityResource


blueprint = Blueprint("api", __name__)

ObservableResource.register(blueprint)
EntityResource.register(blueprint)
