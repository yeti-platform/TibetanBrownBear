from yeti.core.model.settings.setting import Setting
from yeti.core.errors import RuntimeException


class Vocabs(Setting):
    """This object interacts with vocabularies stored in Yeti.

    Attributes:
      name: Name of the Vocab setting
    """

    type = 'vocab'

    def get_vocab(self):
        """Returns content of a given vocab.

        Raises:
          RuntimeException: When no vocab with that name is defined.
        """
        if self.name not in self.settings:
            raise RuntimeException('{0:s} is not a defined vocabulary'.format(
                self.name))
        return self.settings[self.name]

    def set_vocab(self, vocab_list):
        """Sets the vocab list."""
        self.settings[self.name] = vocab_list
        self.save()

    def add_value_to_vocab(self, value):
        """Adds a vocabulary item to a given vocab."""
        if not self.name in self.settings:
            self.settings[self.name] = []
        if value not in self.settings[self.name]:
            self.settings[self.name].append(value)
            self.save()

    def remove_value_from_vocab(self, value):
        """Removes a value from a vocab.

        Args:
          value: The value to remove.

        Raises:
          RuntimeException: A vocab is not defined or the vocab is not
              in the vocab list.
        """
        if self.name not in self.settings:
            raise RuntimeException('{0:s} is not a defined vocabulary'.format(
                self.name))
        if value not in self.settings[self.name]:
            raise RuntimeException('"{0:s}" not in vocab {1:s}'.format(
                value, self.name))
        self.settings[self.name].remove(value)
        self.save()

    def filter_values_vocab(self, value_filter):
        """Returns a filtered list of vocabulary items.

        Args:
          value_filter: string to filter vocabs with.
        """
        selected_values = []
        for value in self.settings[self.name]:
            if value_filter in value:
                selected_values.append(value)
        return selected_values

Setting.datatypes[Vocabs.type] = Vocabs
