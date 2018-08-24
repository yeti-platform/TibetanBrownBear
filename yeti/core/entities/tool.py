"""Detail Yeti's Tool object structure."""

from .entity import Entity

class Tool(Entity):
    """Tool Yeti object.

    Extends the Tool STIX2 definition.
    """

    _collection_name = 'entities'
    type = 'tool'

    @property
    def name(self):
        return self._stix_object.name

    @property
    def description(self):
        return self._stix_object.description

    @property
    def kill_chain_phases(self):
        return self._stix_object.kill_chain_phases

    @property
    def tool_version(self):
        return self._stix_object.tool_version

Entity.datatypes[Tool.type] = Tool
