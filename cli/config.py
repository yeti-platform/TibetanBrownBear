import configparser
from pathlib import Path

class ClientConfig:

    def __init__(self):
        self.api_base = None
        self.api_key = None
        self.loaded = False

    def load_config(self):

        parser = configparser.ConfigParser()
        configfile = Path(Path.home(), '.yetirc')
        if not configfile.exists():
            print(f'{configfile} does not exist.')
            self.loaded = False

        try:
            parser.read(configfile)
            self.api_base = parser.get('server', 'api_base')
            self.api_key = parser.get('authentication', 'api_key')
        except configparser.NoSectionError as error:
            print(f'Error while parsing {configfile}: {error}')
            exit(-1)

        if not self.api_base:
            print(f'No api_base definition found in {configfile}, bailing')
            exit(-1)

        if not self.api_key:
            print(f'No api_key definition found in {configfile}, bailing')
            exit(-1)

        self.loaded = True

config = ClientConfig()
config.load_config()
