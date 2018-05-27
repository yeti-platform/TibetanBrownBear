"""API endpionts for Yeti."""

from flask import Blueprint

from yeti.common.config import yeti_config

from .observable import ObservableResource
from .entity import EntityResource
from .indicator import IndicatorResource
from .tag import TagResource
from .async import AsyncResource

blueprint = Blueprint('api', __name__)

ObservableResource.register(blueprint)
EntityResource.register(blueprint)
IndicatorResource.register(blueprint)
TagResource.register(blueprint)

if yeti_config.async.enabled:
    AsyncResource.register(blueprint)
