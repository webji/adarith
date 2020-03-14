
import os

import pygame as pg

from .annotation import Singleton
from .director import Director
from .configure import Configure

class ApplicationProtocol(object):
    def application_did_finish_launching(self):
        pass

    def application_did_enter_background(self):
        pass

    def application_will_enter_foreground(self):
        pass

    def set_animation_Interval(self):
        pass

    def get_target_platform(self):
        pass

    def get_version(self):
        pass

    def open_url(self):
        pass


@Singleton
class Application(ApplicationProtocol):
    def __init__(self):
        self.animation_interval = 1.0/60.0*1000.0
        self.main_path = None
        self.res_path = None
        self.config_path = None
        self.should_end = False
        self.clock = pg.time.Clock()
        super().__init__()

    def run(self):
        if not self.application_did_finish_launching():
            return -1
        
        if self.main_path == None:
            self.main_path = os.path.join(__file__)
        
        self.res_path = os.path.join(self.main_path, 'res')
        self.config_path = os.path.join(self.main_path, 'conf')
        
        # init config
        config = Configure()
        config.load(self.config_path)

        last_time = 0
        cur_time = 0

        director = Director()
        director.load_config(self.config_path)
        
        while not self.should_end:
            last_time = pg.time.get_ticks()
            director.main_loop()
            cur_time = pg.time.get_ticks()

    
    def end(self):
        self.should_end = True


    

