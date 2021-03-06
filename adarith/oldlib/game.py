#!/usr/bin/env python

"""
Base of Game Class
"""

try:
    import sys, random, math, os, getopt
    import pygame as pg
    from socket import *
    from pygame.locals import *

    from .scene import Scene
    from .utils import *
    from .sound import Sound

except ImportError as e:
    print(f'Failed to load module: {e}')
    sys.exit(2)


class GameBase(object):
    def __init__(self, path='', screen=DEFAULT_SCREEN, bg_color=DEFAULT_BACKGROUND, caption=DEFAULT_CAPTION, fps=DEFAULT_FPS, **kwargs):
        self.scene = Scene()
        self._init_path(path=path)
        self._init_screen(screen=screen, caption=caption)
        self._init_res()
        self._init_players()
        self._init_atlas()
        self._init_sprites()
        self._init_scenes()
        self._init_background(bg_color=bg_color)
        self._post_init(kwargs=kwargs)
        super().__init__()

    def _init_path(self, path=''):
        self.main_dir = path
        self.res_dir = os.path.join(path, 'res')
        self.image_dir = os.path.join(self.res_dir, 'image')
        self.sound_dir = os.path.join(self.res_dir, 'sound')
        
        
    def _init_screen(self, screen=DEFAULT_SCREEN, caption=DEFAULT_CAPTION):
        pg.init()
        pg.mixer.init()
        self.bg_music = None
        self.key_sound = Sound(path=None)
        self.bg_image = None
        self.screen = pg.display.set_mode(screen) #, pg.FULLSCREEN)
        pg.display.set_caption(caption)

    def _init_res(self):
        pass

    
    def _init_players(self):
        pass
        

    def _init_atlas(self):
        pass


    def _init_sprites(self):
        pass

    
    def _init_scenes(self):
        pass

    def _fill_backgroupd(self):
        if (self.bg_image != None):
            self.screen.fill(self.bg_color)
            self.screen.blit(self.bg_image, self.bg_image.get_rect())
        else:
            self.background.fill(self.bg_color)
            self.screen.blit(self.background, (0, 0))
        

    def _init_background(self, bg_color=DEFAULT_BACKGROUND, fps=DEFAULT_FPS):
        self.bg_color = bg_color
        self.clock = pg.time.Clock()
        self.fps = fps
        background = pg.Surface(self.screen.get_size())
        self.background = background.convert()
        self._fill_backgroupd()
        pg.display.flip()
        


    def _post_init(self, **kwargs):
        pass

    
    def _pre_run(self, **kwargs):
        pass

    def _handle_event(self, event=None):
        pass

    def _update_screen(self):
        pass

    def _pre_quit(self, **kwargs):
        pass


    def run(self, **kwargs):

        self._pre_run(kwargs=kwargs)
        self.bg_music = self.scene.bg_music
        pg.mixer.music.load(self.bg_music)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(loops = -1)

        while self.scene:
            self.clock.tick(self.fps)
            events = []
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    self.key_sound.play()
                if event.type == QUIT:
                    self.scene.end()
                    self._pre_quit(kwargs=kwargs)
                    return
                else:
                    events.append(event)

            if self.scene.next.bg_image != None and self.bg_image != self.scene.next.bg_image:
                self.bg_image = self.scene.next.bg_image
            
            self._fill_backgroupd()
                
            self.scene.process_input(events)
            self.scene.update()
            self.scene.draw(self.screen)

            pg.display.flip()

            if self.scene.next.bg_music != None and self.scene.bg_music != self.scene.next.bg_music :
                pg.mixer.music.stop()
                pg.mixer.music.load(self.scene.next.bg_music)
                pg.mixer.music.play(loops = -1)

            self.scene = self.scene.next
            
        

    