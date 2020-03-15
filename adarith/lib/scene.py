from .node import Node

from .core import CGSize, CGPoint

class Scene(Node):
    
    @classmethod
    def create(cls):
        scene = Scene()
        scene._init()
        return scene
    
    @classmethod
    def create(cls, size:CGSize=None):
        scene = Scene()
        scene._init_with_size(size)
        return scene

    def get_description(self):
        return f'<Scene, tag={self.tag}, name={self.name}>'

    def _init(self):
        self.set_ignore_anchor_point_for_position(True)
        self.set_anchor_point(CGPoint(0.5, 0.5))
        size = self.director.get_win_size()
        return self.init_with_size(size)

    def _init_with_size(self, size:CGSize=None):
        self._init()
        self.set_content_size(size)    


class TransitionScene(Scene):
    pass