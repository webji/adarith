from enum import IntEnum
# TODO shoudl change to sortedcontainers using SortedDict
from collections import OrderedDict

from .utils import *
from .core import CGPoint, CGSize, CGRect

from .actionmanager import ActionManager
from .scheduler import Scheduler
# from .event import EventDispatcher



class NodeFlags(IntEnum):
    FLAGS_TRANSFORM_DIRTY = (1 << 0)
    FLAGS_CONTENT_SIZE_DIRTY = (1 << 1)
    FLAGS_RENDER_AS_3D = (1 << 3)
    FLAGS_DIRTY_MASK = (FLAGS_TRANSFORM_DIRTY | FLAGS_CONTENT_SIZE_DIRTY)


class Node(object):
    INVALID_TAG = -1

    def __init__(self):
        from .director import Director

        self.director = Director()
        self.action_manager = self.director.action_manager
        self.scheduler = self.director.scheduler
        self.event_dispatcher = self.director.event_dispatcher
        self.render = self.director.render

        self.children = OrderedDict()
        self._running = False
        self._attached_node_count = 0
        self._on_enter_callback = None

        self._tranform_updated = False
        self._tranform_dirty = False
        self._inverse_dirty = False

        self.tag = Node.INVALID_TAG
        self.name = None
        self.local_z = None
        self.user_data = None
        self.user_object = None

        self._skew_x = 0.0
        self._skew_y = 0.0

        self._rotation_zx = 0.0
        self._rotation_zy = 0.0

        self._scale_x = 1.0
        self._scale_y = 1.0
        self._scale_z = 1.0

        self._normalized_position = CGPoint()
        self._position_z = 0.0
        self._position = CGPoint()

        self._parent = None
        self._visible = True
        self._content_size = CGSize()
        self._ignore_anchor_point_for_position=True
        self._anchor_point = CGPoint(0.5, 0.5)
        self._anchor_point_in_points = CGPoint(self._content_size.w * self._anchor_point.x, self._content_size.h * self._anchor_point.y)
        self._order_of_arrival = 0

    
        super().__init__()


    

    def _not_self_child(self, node=None):
        check_none(node)
        parent = self.parent
        while parent:
            if parent == node:
                return False
            parent = parent.parent
        return True


    def cleanup(self):
        self.stop_all_actions()
        self.unschedule_all_callbacks()

        for node in self.children.values():
            node.cleanup()


    """
    skew
    """
    def get_skew_x(self):
        return self._skew_x


    def set_skew_x(self, x):
        if self._skew_x == x:
            return
        self._skew_x = x
        self._tranform_updated = self._transform_dirty = self._inverse_dirty = True


    def get_skew_y(self):
        return self._skew_y


    def set_skew_y(self, y):
        if self._skew_y == y:
            return
        self._skew_y = y
        self._tranform_updated = self._transform_dirty = self._inverse_dirty = True





    """
    z-order
    """    
    def set_local_z(self, z):
        if self._local_z == z:
            return

        self._local_z = z
        if self._parent:
            self._parent.reorder_child(self, z)
        self._event_dispatcher.set_dirty_for_node(self)
    
    def set_global_z(self, z):
        if self._global_z == z:
            return

        self._global_z = z
        self._event_dispatcher.set_dirty_for_node(self)

    """
    rotation
    """
    def get_rotation(self):
        check(self._rotation_zx == self._rotation_zy, 'Node#rotation. rotation_zx != rotation_zy. Donnt know which one to return')
        return self._retotatioin_zx


    def set_rotation(self, rotation:float):
        if self._rotation_zx == rotation:
            return
        self._rotation_zx = self._rotation_zy = rotation
        self.update_rotation_quat()

    def get_rotation_skew_x(self):
        return self._rotation_zx

    def get_rotation_skew_y(self):
        return self._rotation_zy

    
    def update_rotation_quat(self):
        # TODO calculate the rotation
        pass


    """
    scale
    """
    def get_scale(self):
        check(self._scale_x == self._scale_y, 'Node#Scale. scale_x != scale_y. Donnt know which one to return')
        return self._scale_x

    def set_scale(self, scale:float=None):
        if self._scale_x == self._scale_y == self._scale_z == scale:
            return

        self._scale_x = self._scale_y = self._scale_z = scale
        self._tranform_updated = self._transform_dirty = self._inverse_dirty = True


    def set_scale_xy(self, scale_x, scale_y):
        if self._scale_x == scale_x and self._scale_y == scale_y:
            return

        self._scale_x = scale_x
        self._scale_y = scale_y
        self._tranform_updated = self._transform_dirty = self._inverse_dirty = True

    def set_scale_x(self, scale_x):
        self.set_scale_xy(scale_x, self._scale_y)

    def set_scale_y(self, scale_y):
        self.set_scale_xy(self._scale_x, scale_y)

    def set_scale_z(self, scale_z):
        if self._scale_z == scale_z:
            return
        
        self._scale_z = scale_z
        self._tranform_updated = self._transform_dirty = self._inverse_dirty = True


    def get_position(self):
        return self._position

    def get_position_x(self):
        return self._position.x

    def set_position_x(self, x):
        self.set_position_xy(x, self._position.y)

    
    def get_position_y(self):
        return self._position.y

    def set_position_y(self, y):
        self.set_position_xy(self._position.x, y)

    def set_position_xy(self, x, y):
        if self._position.x == x and self._position.y == y:
            return

        self._position.x = x
        self._position.y = y

        self._tranform_updated = self._transform_dirty = self._inverse_dirty = True
        self._use_normalized_position = False


    def set_position(self, position:CGPoint=None):
        self.set_position_xy(position.x, position.y)    

    def get_normalized_position(self):
        return self._normalized_position

    def set_normalized_position(self, position:CGPoint=None):
        if self._normalized_position == position:
            return
        self._normalized_position = position
        self._use_normalized_position = True
        self._normalized_positon_dirty = True
        self._tranform_updated = self._transform_dirty = self._inverse_dirty = True


    def get_visible(self):
        return self._visible

    def set_visible(self, visible:bool=None):
        if self._visible != visible:
            self._visible = visible
            if self._visible:
                self._tranform_updated = self._transform_dirty = self._inverse_dirty = True



    def get_anchor_point(self):
        return self._anchor_point


    def set_anchor_point(self, point:CGPoint=None):
        if self._anchor_point != point:
            self._anchor_point = point
            self._anchor_point_in_points = CGPoint(self.content_size.w * self.anchor_point.x, self.content_size.h * self.anchor_point.y)
            self._tranform_updated = self._transform_dirty = self._inverse_dirty = True


    def get_content_size(self):
        return self._content_size
    
    def set_content_size(self, size:CGSize=None):
        if self._content_size != size:
            self._content_size = size
            self._anchor_point_in_points = CGPoint(self.content_size.w * self.anchor_point.x, self.content_size.h * self.anchor_point.y)
            self._tranform_updated = self._transform_dirty = self._inverse_dirty = True


    def get_parent(self):
        return self._parent

    def set_parent(self, parent=None):
        self._parent = parent
        self._tranform_updated = self._transform_dirty = self._inverse_dirty = True

    

    def get_ignore_anchor_point_for_position(self):
        return self._ignore_anchor_point_for_position


    def set_ignore_anchor_point_for_position(self, ignore:bool=None):
        if self._ignore_anchor_point_for_position == ignore:
            self._ignore_anchor_point_for_position = ignore
            self._tranform_updated = self._transform_dirty = self._inverse_dirty = True



    def get_order_of_arrival(self):
        return self._order_of_arrival

    def set_order_of_arrival(self, order:int=None):
        check(order > 0, 'Invalid order_of_arrival')
        self._order_of_arrival = order


    def get_scene(self):
        if self._parent == None:
            return None
        
        scene_node = self._parent
        while(scene_node.get_parent()):
            scene_node = scene_node.get_parent()
        return scene_node


    def get_bounding_box(self):
        rect = CGRect(0, 0, self._content_size.w, self._content_size.h)
        return rect

    def get_child_by_tag(self, tag:int=INVALID_TAG):
        check(tag != INVALID_TAG, 'Invalid tag')
        for child in self.children.values():
            if child and child.tag == tag:
                return child
    

    def get_child_by_name(self, name:str=None):
        check(name and len(name) > 0, 'Invalid name')
        for child in self.children.values():
            if child and child.name == name:
                return child


    def add_child(self, child=None, local_z:int=None, tag:int=INVALID_TAG, name:str=''):
        check(child != None, 'child must not be None')
        check(child._parent == None, "child already added. It can't be added again")
        check(self._not_self_child(child), 'A node cannot be the child of his own children')

        if local_z == None:
            local_z = child.local_z

        self.insert_chiild(child, local_z)
        if tag != INVALID_TAG:
            child.tag = tag
        
        if len(name) > 0:
            child.name = name
        
        child.set_parent(self)

        if self._running:
            child.on_enter()
            if self._is_transition_finished:
                child.on_enter_transition_did_finished()
        
        if self._cascade_color_enabled:
            self.update_cascade_color()

        if self._cascade_opacity_enabled:
            self.update_cascade_opacity()


    def remove_from_parent(self):
        self.remove_from_parent_and_cleanup(True)

    
    def remove_from_parent_and_cleanup(self, cleanup:bool=True):
        if self._parent:
            self._parent.remove_child(self, cleanup)

    
    def remove_child(self, child=None, cleanup:bool=True):
        if len(self.children) <= 0:
            return
        self.detach_child(child, cleanup)


    def remove_child_by_tag(self, tag:int=None, cleanup:bool=True):
        check(tag != INVALID_TAG, 'Invalid tag')
        child = self.get_child_by_tag(tag)
        if child:
            raise pg.error(f'remove_child_by_tag({tag}): child not found')
        self.remove_child(child, cleanup)

    def remove_child_by_name(self, name:str=None, cleanup:bool=True):
        check(name and len(name), 'Invalid name')
        child = self.get_child_by_name(name)
        if child:
            raise pg.error(f'remove_child_by_name({name}): child not found')
        self.remove_child(child, cleanup)
        

    def remove_allchildren(self, cleanup:bool=True):
        for child in self.children.values():
            if self._running:
                child.on_exit_transition_did_start()
                child.on_exit()
            
            if cleanup:
                child.cleanup()
            child.set_parent(None)
            self.children.clear()



    def detach_child(self, child=None, cleanup:bool=True):
        check_none(child)
        check_none(cleanup)
        if self._running:
            child.on_exit_transition_did_start()
            child.on_exit()

        if cleanup:
            child.cleanup()

        child.set_parent(None)
        self.children[child.get_local_z()] = None


    def insert_chiild(self, node=None, z:int = None):
        node.set_local_z(z)
        self.children[z] = node


    def draw(self, render=None):
        pass
    
    def visit(self):
        self.draw(self._render)


    # TODO Implement 
    def visit(self, renderer, parent_transform, parent_flags):
        if not self._visible:
            return

        self_visited = False
        if len(self.children) > 0:
            for k in self.children.keys():
                node = self.children[k]
                if node and node._local_z < 0:
                    node.visit(self._render)
                else:
                    if not self_visited and self._visible:
                        self.draw(self._render)
                        self_visited = True
                    else:
                        node.visit(self._render)



    def resume(self):
        self._scheduler.resume_target(self)
        self._action_manager.resume_target(self)
        self._event_dispatcher.resume_event_listeners_for_target(self)

    
    def pause(self):
        self._scheduler.pause_target(self)
        self._action_manager.resume_target(self)
        self._event_dispatcher.pause_event_listeners_for_target(self)

    


    def on_enter(self):
        if not self._running:
            self._attached_node_count += 1

        if self._on_enter_callback:
            self._on_enter_callback()

        self._is_transition_finished = False
        for node in self.children.values():
            node.on_enter()
        
        self.resumme()
        self._running = True

    def on_enter_transition_did_finished(self):
        if self._on_enter_transition_didS_finish_callback:
            self._on_enter_transition_did_finish_callback()
        self._is_transition_finished = True

        for node in self.children.values():
            node.on_enter_transition_did_finished()


    def on_exit_transition_did_start(self):
        if self._on_exit_transition_did_start:
            self._on_exit_transition_did_start()
        
        for node in self.children.values():
            node.no_exit_transition_did_start()


    def on_exit(self):
        if self._running:
            self._attached_node_count -= 1
        
        if self._on_exit_callback:
            self._on_exit_callback()

        self.pause()

        self._running = False

        for node in self.children.values():
            node.on_exit()



    def set_event_dispatcher(self, dispatcher=None):
        if self._event_dispatcher != dispatcher:
            self._event_dispatcher.remove_event_listeners_for_target(self)
            self._event_dispatcher = dispatcher


    def set_action_manager(self, action_manager:ActionManager=None):
        if self._action_manager != action_manager:
            self.stop_all_actions()
            self._action_manager = action_manager


    def run_action(self, action):
        check(action != None, 'action must not be None')
        self._action_manager.add_action(action, self, not self._running)
        return action


    def stop_all_actions(self):
        self._action_manager.remove_all_actions_from_target(self)

    
    def stop_action(self, action=None):
        self._action_manager.remove_action(action)


    

    