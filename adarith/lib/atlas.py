#!/usr/bin.env python
"""
Altas of the whold world
"""

import os, sys
import pygame
from pygame.locals import *



class Atlas(object):
    def __init__(self):
        self._prepare()

        super().__init__()
    

    def _prepare(self):
        if not pygame.font: print('Warning, fonts disabled')
        if not pygame.mixer: print('Warning, sound disabled')

    def _init(self):
        pygame.sprite.Sprite.__init__(self)
        
    
    def _init_screen(self):
        pass

    def _load_image(self, name, colorKey=None):
        pass