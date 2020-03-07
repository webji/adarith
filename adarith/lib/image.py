#!/user/bin/env python
import pygame
from pygame.locals import RLEACCEL
from pygame.compat import geterror

class Image(object):
    def __init__(self, path, colorKey=None):
        try:
            image = pygame.image.load(path)
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error as e:
            print(f'Failed to load image: [path={path}][colorKey={colorKey}][error={e}]')
            raise SystemExit(str(geterror()))

        if colorKey is not None:
            if colorKey == -1:
                colorKey = image.get_at((0, 0))
            image.set_colorkey(colorKey, RLEACCEL)

        self.image = image
        self.rect = image.get_rect()
        super().__init__()

