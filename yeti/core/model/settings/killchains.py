from yeti.core.model.settings.setting import Setting

from yeti.core.errors import RuntimeException


class KillChains(Setting):
    """This object interacts with killchainularies stored in Yeti.

    Attributes:
      name: Name of the killchain setting
    """

    type = 'killchain'

    def get_killchain(self):
        """Gets a specific killchain's contents.

        Raises:
          RuntimeException: When no killchain with that name is defined.
        """
        if self.name not in self.settings:
            raise RuntimeException('{0:s} is not a defined killchain'.format(
                self.name))
        return self.settings[self.name]

    def set_phases(self, killchain_list):
        """Sets the killchain phases."""
        self.settings[self.name] = killchain_list
        self.save()

    def add_phase_to_killchain(self, phase):
        """Adds a killchain phase to a given killchain."""
        if not self.name in self.settings:
            self.settings[self.name] = []
        if phase not in self.settings[self.name]:
            self.settings[self.name].append(phase)
            self.save()

    def remove_phase_from_killchain(self, phase):
        """Removes a phase from a killchain.

        Args:
          phase: The phase to remove.

        Raises:
          RuntimeException: A killchain is not defined or the killchain is not
              in the killchain list.
        """
        if self.name not in self.settings:
            raise RuntimeException('{0:s} is not a defined killchain'.format(
                self.name))
        if phase not in self.settings[self.name]:
            raise RuntimeException('"{0:s}" not in killchain {1:s}'.format(
                phase, self.name))
        self.settings[self.name].remove(phase)
        self.save()

    def filter_phase_killchain(self, phase_filter):
        """Returns a filtered list of killchain items.

        Args:
          phase_filter: string to filter KillChain phases with.
        """
        selected_phases = []
        for phase in self.settings[self.name]:
            if phase_filter in phase:
                selected_phases.append(phase)
        return selected_phases

Setting.datatypes[KillChains.type] = KillChains
