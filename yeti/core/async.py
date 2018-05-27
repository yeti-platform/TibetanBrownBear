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
    settings = None
    enabled = False
    period = None
    last_executed = None

class AsyncJob(ABC):

    def __init__(self):
        self.reload_settings()

    @abstractmethod
    def execute(self):
        """Executes an AsyncJob.

        This contains the actual functionality of the AsyncJob.
        It should be defined in all classes extending AsyncJob
        """
        raise NotImplementedError

    @classmethod
    def create(cls, *args, **kwargs):
        """Creates and executes a given AsyncJob."""
        job = cls(*args, **kwargs)
        return job.execute()

    def save_settings(self):
        """Saves setting information to the database."""
        self.settings.save()

    def reload_settings(self):
        """Fetches setting information from the database."""
        self.settings = AsyncJobSettings.get_or_create(name=self.name)

    @property
    def name(self):
        """Returns the name of the class."""
        return self.__class__.__name__

    def dump(self):
        """Returns a JSON dump of the Async job's settings."""
        return self.settings.dump()
