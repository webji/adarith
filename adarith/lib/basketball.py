#!/user/bin/env python
import pygame, math

from .image import Image


class BasketBall(pygame.sprite.Sprite):
    """
    A Basketball
    """

    def __init__(self, path='', vector=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        image = Image(path=path)
        self.image = image.image
        self.rect = image.rect
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.hit = 0
        super().__init__()

    def update(self, player1=None, player2=None):
        newpos = self._calc_newpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if tr and tl or ( br and bl):
                angle = -angle
            if tl and bl:
                angle = math.pi - angle
            if tr and br:
                angle = math.pi - angle
        elif player1  and player2 :
            player1.rect.inflate(-3, -3)
            player2.rect.inflate(-3, -3)

            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit
        self.vector = (angle, z)

    

    def _calc_newpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z*math.cos(angle), z*math.sin(angle))
        return rect.move(dx, dy)