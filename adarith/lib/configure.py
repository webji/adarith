
from .annotation import Singleton

@Singleton
class Configure(object):
    DEFAULT_FPS = 60.0
    
    def __init__(self):
        self._configs = {}
        super().__init__()

    def load(self, path):
        with open(path) as fp:
            for line in fp.readlines():
                k, v = line.strip().split('=')
                self._configs[k] = v
    
    def get_value(self, key:str, default_value=None):
        ret = self._configs[key]
        return ret if ret else default_value

    