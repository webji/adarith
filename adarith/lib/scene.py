#!/usr/bin/env python

"""
Base of Scene Class
"""
import pygame as pg
from pygame.locals import *

from .utils import *

class SceneBase(object):
    def __init__(self, id='default_scene', name='Default Sene', bg_color=BLACK, font_color=WHITE, bg_music=None):
        self.id = id
        self.name = name
        self.bg_color = bg_color
        self.font_color = font_color
        self.bg_music = bg_music
        self.nextScenes = {}
        self.prev = self
        self.next = self
        super().__init__()


    def add_next(self, key, scene):
        self.nextScenes[key] = scene
        return self
    
    def _pre_enter(self, **kwarg):
        pass

    def _pre_leave(self, **kwargs):
        pass

    def _pre_end(self):
        pass

    def enter(self, **kwargs):
        self._pre_enter(kwargs=kwargs)

   
    def leave(self, **kwargs):
        pass
            

    def update(self):
        pass
    
    def draw(self, screen):
        screen.fill(self.bg_color)
        size = screen.get_size()
        width = size[0]
        height = size[1]
        draw_text(screen, "Default Scene", 50, self.font_color, width/2, height/2, align='center')
        draw_text(screen, "press <q> to end", 20, self.font_color, width / 2, height * 3 / 4, align="center")
        draw_text(screen, "press <any> for stay", 20, self.font_color, width / 2, height * 3 / 4 + 50, align="center")


    def switch_to(self, next_scene):
        next_scene.prev = self
        next_scene.next = next_scene
        self.next = next_scene
        self._pre_leave()       
        next_scene._pre_enter() 
        print(f'switch from {self.id} to {next_scene.id}')


    def end(self):
        self._pre_end()
        self.next = None

    
    def _handle_switch_scene(self, event):
        next = self
        if event.key == K_LEFT:
            next = self.prev
        elif event.key in self.nextScenes.keys():
            next = self.nextScenes[event.key]
        
        self.switch_to(next)


    def _handle_scene_event(self, event):
        pass
        # print(f'Handle Scene Event: {self}: {event}')

    def process_input(self, events):
        for event in events:
            if event.type == pg.KEYUP and (event.key in self.nextScenes.keys() or event.key == K_LEFT):
                self._handle_switch_scene(event)
            else:
                self._handle_scene_event(event)

