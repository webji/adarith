
from .singleton import Singleton

class Configure(Singleton):
    DEFAULT_FPS = 60.0
    
    def init(self):
        self._configs = {}
        

    def load(self, path):
        with open(path) as fp:
            for line in fp.readlines():
                k, v = line.strip().split('=')
                self._configs[k.strip()] = v.strip()
    
    def get_value(self, key:str, default_value=None):
        ret = self._configs[key]
        return ret if ret else default_value

    def get_float(self, key:str, default_value:float=None):
        ret = self._configs[key]
        return float(ret) if ret else default_value

    