
from .singleton import Singleton
class Render(Singleton):

    def init(self):
        self._is_rendering = False
    
    def begin_frame(self):
        print(f'render begin frame')

    def end_frame(self):
        print(f'render end frame')
        
    def render(self):
        self._is_rendering = True

