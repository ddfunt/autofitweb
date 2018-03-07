import os
import autofit

class Paths:

    @classmethod
    def db_path(cls):
        folder = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Autofit')
        if not os.path.isdir(folder):
            os.mkdir(folder)
        return os.path.join(folder, 'gauss.db')
    @classmethod
    def spcat(cls):
        return os.path.join(os.path.expanduser('~'), 'AppData', 'local', 'BrightSpec', 'SPCAT')

    @classmethod
    def config_path(cls):

        return os.path.join(Paths.repo_root(), 'config.ini')

    @classmethod
    def package_root(cls):
        root = os.path.dirname(autofit.__file__)
        return root

    @classmethod
    def repo_root(cls):
        return os.path.split(Paths.package_root())[0]

if __name__ == '__main__':
    print(Paths.repo_root())
    print(Paths.db_path())