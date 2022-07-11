"""API endpionts for Yeti."""

from flask import Blueprint

from yeti.common.config import yeti_config

from .observable import ObservableResource
from .entity import EntityResource
from .indicator import IndicatorResource
from .tag import TagResource
from .asyncjob import AsyncResource
from .settings import SettingsResource
from .relationship import RelationshipResource

blueprint = Blueprint('api', __name__)

ObservableResource.register(blueprint)
EntityResource.register(blueprint)
IndicatorResource.register(blueprint)
TagResource.register(blueprint)
SettingsResource.register(blueprint)
RelationshipResource.register(blueprint)

if yeti_config.asyncjob.enabled:
    AsyncResource.register(blueprint)

try:
    if yeti_config.core.auth == 'oidc':
        from yeti.auth.oidc.views import UserResource
    if yeti_config.core.auth == 'local':
        from yeti.auth.local.views import UserResource
except Exception as e:
    raise(f'{e}\n\n{yeti_config.core}')
UserResource.register(blueprint)
