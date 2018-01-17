"""YetiConnector interface.

This interface defines the methods a YetiConnector needs to implement to
successfully carry out all interactions with the database.
"""

from abc import abstractmethod, ABC

class AbstractYetiConnector(ABC):

    @classmethod
    @abstractmethod
    def load(cls, args):
        """Load a YetiObject from its JSON representation."""
        raise NotImplementedError

    @abstractmethod
    def dump(self):
        """Dump a YetiObject into its JSON representation."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def dump_many(cls, objects):
        """Dump a list of YetiObject into its JSON representation."""
        raise NotImplementedError

    @abstractmethod
    def save(self):
        """Inserts a Yeti object into the database.

        Returns:
          The created Yeti object."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def list(cls):
        """Lists all objects.

        Returns:
          A list of objects contained in the database."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get(cls, key):
        """Fetches a single object by primary key.

        Args:
          key: A database primary key value.

        Returns:
          A Yeti object."""
        raise NotImplementedError


    @classmethod
    def filter(cls, args):
        """Filters objects according to args.

        Args:
          args: parameters used to filter the objects.
        """
        raise NotImplementedError
