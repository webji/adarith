from enum import IntEnum
# TODO shoudl change to sortedcontainers using SortedDict
from collections import OrderedDict

from .utils import *

from .director import Director
from .actionmanager import ActionManager
from .scheduler import Scheduler
from .eventdispatcher import EventDispatcher



class NodeFlags(IntEnum):
    FLAGS_TRANSFORM_DIRTY = (1 << 0)
    FLAGS_CONTENT_SIZE_DIRTY = (1 << 1)
    FLAGS_RENDER_AS_3D = (1 << 3)
    FLAGS_DIRTY_MASK = (NodeFlags.FLAGS_TRANSFORM_DIRTY | NodeFlags.FLAGS_CONTENT_SIZE_DIRTY)


class Node(object):
    INVALID_TAG = -1

    def __init__(self):
        self._director = Director()
        self._action_manager = self._director._action_manager
        self._scheduler = self._director._scheduler
        self._event_dispatcher = self._director._event_dispatcher
        self._render = self._director._render

        self._visible = True
        self.children = OrderedDict()
        self._running = False
        self._attached_node_count = 0
        self._on_enter_callback = None

        self.parent = None
        self.tag = INVALID_TAG
        self.name = None
        self.local_z = None
        # self._transform = None
        # self._inverse = None
        # self._model_view_transform = None
        super().__init__()


    def _not_self_child(self, node:Node=None):
        check_none(node)
        parent = self.parent
        while parent:
            if parent == node:
                return False
            parent = parent.parent
        return True


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


    def add_child(self, child:Node=None, local_z:int=None, tag:int=INVALID_TAG, name:str=''):
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

    
    def remove_child(self, child:Node=None, cleanup:bool=True):
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



    def detach_child(self, child:Node=None, cleanup:bool=True):
        check_none(child)
        check_none(cleanup)
        if self._running:
            child.on_exit_transition_did_start()
            child.on_exit()

        if cleanup:
            child.cleanup()

        child.set_parent(None)
        self.children[child.get_local_z()] = None


    def insert_chiild(self, node:Node=None, z:int = None):
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



    def set_event_dispatcher(self, dispatcher:EventDispatcher=None):
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


    def cleanup(self):
        self.stop_all_actions()
        self.unschedule_all_callbacks()

        for node in self.children.values():
            node.cleanup()


    