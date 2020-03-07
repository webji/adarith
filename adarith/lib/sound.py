#!/user/bin/env python
import pygame
from pygame.locals import RLEACCEL
from pygame.compat import geterror

class NoneSound:
    def play(self):
        pass

class Sound(object):
    def __init__(self, path):
        sound = NoneSound
        if not pygame.mixer or not pygame.mixer.get_init():
            pass
        else:
            try:
                sound = pygame.mixer.Sound(path)
            except pygame.error:
                print(f"Failed to load sound: [path={path}]")
                raise SystemExit(str(geterror))
        self.sound = sound        
        super().__init__()
