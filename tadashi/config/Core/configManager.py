import yaml
import os


class ConfigManager:

    __instance = None

    @staticmethod
    def get_instance():
        if ConfigManager.__instance is None:
            ConfigManager()
        return ConfigManager.__instance

    def __init__(self):
        self._configs = None
        self._absolute_path = os.path.abspath(os.path.dirname(__file__))
        self.load_config()
        ConfigManager.__instance = self

    def load_config(self):
        with open(self._absolute_path + '/../config/config.yaml', 'r') as stream:
            try:
                self._configs = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                raise e

    def get(self, param):
        return self._configs[param]
