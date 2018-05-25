from abc import abstractmethod, ABC

from marshmallow import fields, post_load

from yeti.core.model.fields import RealTimeDelta, RealDateTime
from yeti.core.model.database import YetiSchema, YetiObject

functions = {}

class AsyncJobSettingsSchema(YetiSchema):
    name = fields.String()
    meta = fields.Dict()
    enabled = fields.Boolean()
    period = RealTimeDelta()
    last_executed = RealDateTime()

    @post_load
    def load_async(self, data):
        """Load an AsyncJobSettings object from its JSON representation.

        @post_load means this will be called after each marshmallow.load call.

        Returns:
          The AsyncJobSettings object.
        """
        return AsyncJobSettings(**data)

class AsyncJobSettings(YetiObject):

    schema = AsyncJobSettingsSchema
    _collection_name = 'asyncjobsettings'
    _indexes = [
        {'fields': ['name'], 'unique': True},
    ]

    id = None
    settings = {}
    enabled = False
    period = None
    last_executed = None

class AsyncJob(ABC):

    def __init__(self):
        self.reload_settings()

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @classmethod
    def create(cls, *args, **kwargs):
        job = cls(*args, **kwargs)
        return job.execute()

    def save_settings(self):
        self.settings.save()

    def reload_settings(self):
        self.settings = AsyncJobSettings.get_or_create(name=self.name)

    @property
    def name(self):
        return self.__class__.__name__
