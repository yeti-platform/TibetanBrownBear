from yeti.core.model.settings.setting import Setting
from yeti.core.errors import RuntimeException


class Vocabs(Setting):
    """This object interacts with vocabularies stored in Yeti.

    Attributes:
      name: Name of the Vocab setting
      created_at: timestamp when the Tag object was first created.
      default_expiration: Time after which the tag should expire on an Observable.
    """

    name = 'vocabs'

    def get_vocab_for_field(self, field_name):
        """Gets the vocabulary for a given field.

        Args:
          field_name: The name of the field to get the vocabulary for.

        Raises:
          RuntimeException: When no vocab is defined for the field.
        """
        if field_name not in self.settings:
            raise RuntimeException('No vocab defined for field name: {0:s}'.format(
                field_name))
        return self.settings[field_name]

    def set_vocab_for_field(self, field_name, vocab_list):
        """Sets the vocab list for a given field name."""
        self.settings[field_name] = vocab_list
        self.save()

    def add_value_to_field_vocab(self, field_name, value):
        """Adds a vocabulary item for a given field.

        Args:
          field_name: The name of the field to update.
        """
        if not field_name in self.settings:
            self.settings[field_name] = []
        self.settings[field_name].append(value)
        self.save()

    def remove_value_from_field_vocab(self, field_name, value):
        """Removes a value from a vocab list in a field name.

        Args:
          field_name: The field name from which to remove the value.
          value: The value to remove.

        Raises:
          RuntimeException: A vocab for the field is not defined or the vocab is not
              in the vocab list.
        """
        if field_name not in self.settings:
            raise RuntimeException('No vocab for field name: {0:s}'.format(
                field_name))
        if value not in self.settings[field_name]:
            raise RuntimeException('"{0:s}" not in vocab for {1:s}'.format(
                value, field_name))
        self.settings[field_name].remove(value)
        self.save()

    def filter_values_for_field_vocab(self, field_name, value_filter):
        """Returns a filtered list of vocabulary items.

        Args:
          field_name: The name of the field to update.
          value_filter: string to filter vocabs with.
        """
        selected_values = []
        for value in self.settings[field_name]:
            if value_filter in value:
                selected_values.append(value)
        return selected_values

Setting.types[Vocabs.name] = Vocabs
