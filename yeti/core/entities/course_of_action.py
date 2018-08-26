"""Detail Yeti's Course of Action object structure."""

from .entity import Entity

class CourseOfAction(Entity):
    """Course of Action Yeti object.

    Extends the CourseOfAction STIX2 definition.
    """

    _collection_name = 'entities'
    type = 'course-of-action'

    @property
    def name(self):
        return self._stix_object.name

    @property
    def description(self):
        return self._stix_object.description

    @property
    def action(self):
        return self._stix_object.action


Entity.datatypes[CourseOfAction.type] = CourseOfAction
