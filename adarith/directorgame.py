
import os

from lib.application import Application
from lib.director import Director
from lib.scene import Scene

class AppDelegate(Application):

    def application_did_finish_launching(self):
        
        director = Director()
        director._display_stats = True
        director._animation_interval = 1.0/60

        scene = Scene()

        director.run_with_scene(scene)
        return super().application_did_finish_launching()



    def application_did_enter_background(self):
        # return super().application_did_enter_background()
        # from lib.director import Director
        director = Director()
        director.stop_animatioin()

    
    def application_will_enter_foreground(self):
        # from lib.director import Director
        director = Director()
        director.start_animation()


# from lib.singleton import Singleton

# @Singleton
# class Base(Singleton):
#     def __init__(self):
#         self._name = 'base'
#         self.id = 1
#         super().__init__()

#     def __repr__(self):
#         return f'<Base name={self._name}, id={self.id}>'

# class Sub(Base):
#     pass

def main():
#     base1 = Base()

#     base2 = Base()
#     base2.id = 2

#     sub1 = Sub()
#     sub1.id = 3
#     print(f'{base1}')
#     print(f'{base2}')
#     print(f'{sub1}')
    main_path = os.path.split(os.path.abspath(__file__))[0]
    app = AppDelegate()
    app.init(main_path=main_path)

    app.run()


if __name__ == '__main__':
    main()

    
    
    