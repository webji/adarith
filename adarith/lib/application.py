
import os

import pygame as pg

from .utils import *
from .singleton import Singleton
from .configure import Configure
from .director import Director

class ApplicationProtocol(Singleton):
    def application_did_finish_launching(self):
        return True

    def application_did_enter_background(self):
        return True

    def application_will_enter_foreground(self):
        return True

    def set_animation_Interval(self):
        pass

    def get_target_platform(self):
        pass

    def get_version(self):
        pass

    def open_url(self):
        pass


class Application(ApplicationProtocol):

    def init(self, main_path:str=None):
        check_none(main_path)
        pg.init()
        pg.mixer.init()
        
        self.animation_interval = 1.0/60.0*1000.0
        self.main_path = main_path
        self.res_path = os.path.join(self.main_path, 'res')
        self.config_path = os.path.join(self.main_path, 'conf/config.yml')
        self.should_end = False
        self.clock = pg.time.Clock()
    

    def run(self):
        # init config
        config = Configure()
        config.init()
        config.load(self.config_path)

        last_time = 0
        cur_time = 0

        # init director
        director = Director()
        director.init()
        director.application = self
        
        if not self.application_did_finish_launching():
            print('Failed to launch application')
            return -1
        
        while not self.should_end:
            last_time = pg.time.get_ticks()
            director.main_loop()
            cur_time = pg.time.get_ticks()

        director.end()
        director.main_loop()
        director = None

    
    def end(self):
        self.should_end = True


    

