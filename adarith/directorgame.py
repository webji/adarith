from .lib.application import Application
from .lib.director import Director
from .lib.scene import Scene

class AppDelegate(Application):

    def application_did_finish_launching(self):
        director = Director()
        director._display_stats = True
        director._animation_interval = 1.0/60

        scene = Scene()


    def application_did_enter_background(self):
        # return super().application_did_enter_background()
        director = Director()
        director.stop_animatioin()

    
    def application_will_enter_foreground(self):
        director = Director()
        director.start_animation()
        


    

    
    
    