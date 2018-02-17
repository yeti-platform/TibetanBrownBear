"""API endpionts for Yeti."""

from flask import Blueprint

from .observable import ObservableResource
from .entity import EntityResource
from .indicator import IndicatorResource


blueprint = Blueprint("api", __name__)

ObservableResource.register(blueprint)
EntityResource.register(blueprint)
IndicatorResource.register(blueprint)
