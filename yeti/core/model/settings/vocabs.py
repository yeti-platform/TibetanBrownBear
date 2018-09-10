from yeti.core.model.settings.setting import Setting
from yeti.core.errors import RuntimeException


class Vocabs(Setting):
    """This object interacts with vocabularies stored in Yeti.

    Attributes:
      name: Name of the Vocab setting
    """

    name = 'vocabs'

    def get_vocab(self, vocab_name):
        """Gets a specific vocab by name.

        Args:
          vocab_name: The name of the vocab to get.

        Raises:
          RuntimeException: When no vocab with that name is defined.
        """
        if vocab_name not in self.settings:
            raise RuntimeException('{0:s} is not a defined vocabulary'.format(
                vocab_name))
        return self.settings[vocab_name]

    def set_vocab(self, vocab_name, vocab_list):
        """Sets the vocab list."""
        self.settings[vocab_name] = vocab_list
        self.save()

    def add_value_to_vocab(self, vocab_name, value):
        """Adds a vocabulary item for a given vocab.

        Args:
          vocab_name: The name of the vocab to update.
        """
        if not vocab_name in self.settings:
            self.settings[vocab_name] = []
        if value not in self.settings[vocab_name]:
            self.settings[vocab_name].append(value)
            self.save()

    def remove_value_from_vocab(self, vocab_name, value):
        """Removes a value from a vocab.

        Args:
          vocab_name: The vocab from which to remove the value.
          value: The value to remove.

        Raises:
          RuntimeException: A vocab is not defined or the vocab is not
              in the vocab list.
        """
        if vocab_name not in self.settings:
            raise RuntimeException('{0:s} is not a defined vocabulary'.format(
                vocab_name))
        if value not in self.settings[vocab_name]:
            raise RuntimeException('"{0:s}" not in vocab {1:s}'.format(
                value, vocab_name))
        self.settings[vocab_name].remove(value)
        self.save()

    def filter_values_vocab(self, vocab_name, value_filter):
        """Returns a filtered list of vocabulary items.

        Args:
          vocab_name: The name of the vocab to update.
          value_filter: string to filter vocabs with.
        """
        selected_values = []
        for value in self.settings[vocab_name]:
            if value_filter in value:
                selected_values.append(value)
        return selected_values

Setting.types[Vocabs.name] = Vocabs
