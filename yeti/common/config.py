import os
import configparser

from yeti.common.constants import YETI_ROOT


class Dictionary(dict):

    def __getattr__(self, key):
        return self.get(key, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config:

    def __init__(self):
        config = configparser.SafeConfigParser(allow_no_value=True)
        config.read(os.path.join(YETI_ROOT, 'yeti.conf'))

        for section in config.sections():
            setattr(self, section, Dictionary())
            for name in config.options(section):
                try:
                    value = config.getint(section, name)
                except ValueError:
                    try:
                        value = config.getboolean(section, name)
                    except ValueError:
                        value = config.get(section, name)

                getattr(self, section)[name] = value

    def __getitem__(self, key):
        return getattr(self, key)

    def set_default_value(self, section, key, value):
        if not hasattr(self, section):
            setattr(self, section, Dictionary())

        if key not in self[section]:
            self[section][key] = value

    def get(self, section, key, default=None):
        if not hasattr(self, section) or key not in self[section]:
            return default

        return self[section][key]


yeti_config = Config()
yeti_config.set_default_value(
    'arangodb', 'host', os.environ.get('YETI_ARANGO_HOST') or '127.0.0.1')
yeti_config.set_default_value(
    'arangodb', 'port', int(os.environ.get('YETI_ARANGO_PORT', 0)) or 8529)
yeti_config.set_default_value(
    'arangodb', 'database', os.environ.get('YETI_ARANGO_DATABASE') or 'yeti')
yeti_config.set_default_value(
    'arangodb', 'username', os.environ.get('YETI_ARANGO_USERNAME') or 'root')
yeti_config.set_default_value(
    'arangodb', 'password', os.environ.get('YETI_ARANGO_PASSWORD') or '')
