import configparser
from autofit.IO import paths
import collections


class ConfigModel(collections.Mapping):
    """ducktypes as a dictionary settings values
    loaded from a ini file"""

    def __init__(self):
        self._config = self.load_config()

    def load_config(self):
        """loads configureation file from ini
        """
        cfg = configparser.ConfigParser()
        cfg.read(paths.Paths.config_path())
        return cfg

    def __getitem__(self, item):
        return self._config[item]

    def __iter__(self):
        pass

    def __len__(self):
        return len(self._config)



if __name__ == '__main__':
    cfg = ConfigModel()
    print(cfg['SPCAT']['path'])