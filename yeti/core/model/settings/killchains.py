from yeti.core.model.settings.setting import Setting

from yeti.core.errors import RuntimeException


class KillChains(Setting):
    """This object interacts with killchainularies stored in Yeti.

    Attributes:
      name: Name of the killchain setting
    """

    name = 'killchains'

    def get_killchain(self, killchain_name):
        """Gets a specific killchain by name.

        Args:
          killchain_name: The name of the killchain to get.

        Raises:
          RuntimeException: When no killchain with that name is defined.
        """
        if killchain_name not in self.settings:
            raise RuntimeException('{0:s} is not a defined killchain'.format(
                killchain_name))
        return self.settings[killchain_name]

    def set_phases(self, killchain_name, killchain_list):
        """Sets the killchain phases."""
        self.settings[killchain_name] = killchain_list
        self.save()

    def add_phase_to_killchain(self, killchain_name, phase):
        """Adds a killchain phase to a given killchain.

        Args:
          killchain_name: The name of the killchain to update.
        """
        if not killchain_name in self.settings:
            self.settings[killchain_name] = []
        if phase not in self.settings[killchain_name]:
            self.settings[killchain_name].append(phase)
            self.save()

    def remove_phase_from_killchain(self, killchain_name, phase):
        """Removes a phase from a killchain.

        Args:
          killchain_name: The killchain from which to remove the phase.
          phase: The phase to remove.

        Raises:
          RuntimeException: A killchain is not defined or the killchain is not
              in the killchain list.
        """
        if killchain_name not in self.settings:
            raise RuntimeException('{0:s} is not a defined killchain'.format(
                killchain_name))
        if phase not in self.settings[killchain_name]:
            raise RuntimeException('"{0:s}" not in killchain {1:s}'.format(
                phase, killchain_name))
        self.settings[killchain_name].remove(phase)
        self.save()

    def filter_phase_killchain(self, killchain_name, phase_filter):
        """Returns a filtered list of killchain items.

        Args:
          killchain_name: The name of the killchain to filter on.
          phase_filter: string to filter KillChain phases with.
        """
        selected_phases = []
        for phase in self.settings[killchain_name]:
            if phase_filter in phase:
                selected_phases.append(phase)
        return selected_phases

Setting.types[KillChains.name] = KillChains
