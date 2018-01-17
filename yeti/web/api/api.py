"""API endpionts for Yeti."""

from flask import Blueprint
from .observable import ObservableResource

blueprint = Blueprint("api", __name__)

ObservableResource.register(blueprint)
