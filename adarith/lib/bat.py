#!/user/bin/env python
import pygame

from .image import Image

class Bat(pygame.sprite.Sprite):
    """
    bat to hit ball
    Returns: bat object

    """

    def __init__(self, path, side):
        pygame.sprite.Sprite.__init__(self)
        image = Image(path=path)
        self.image = image.image
        self.rect = image.rect

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.side = side
        self.speed = 10
        self.state = "still"
        self.reinit()

        super().__init__()

    
    def reinit(self):
        self.state = 'still'
        self.movepos = [0, 0]
        if self.side == 'left':
            self.rect.midleft = self.area.midleft
        elif self.side == 'right':
            self.rect.midright = self.area.midright
    

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    
    def move_up(self):
        self.movepos[1] = self.movepos[1] - self.speed
        self.state = 'moveup'

    def move_down(self):
        self.movepos[1] = self.movepos[1] + self.speed
        self.state = 'movedown'
