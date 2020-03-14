
from enum import IntEnum
from collections import defaultdict

import pygame as pg

from .utils import *
from .node import Node


"""
EventListener with callback, will be trigered on events occurs
 - type: int
 - is_registered: bool
 - is_fixed_priority: bool
 - is_paused
 - is_enabled
 - on_event: callback
 - node: Node -- the related Node
"""
class EventListener(object):
    EVENT_COME_TO_FOREGROUND = 'event_come_to_foreground'
    EVENT_COME_TO_BACKGROUND = 'event_come_to_background'
    EVENT_RENDERER_RECREATED = 'event_renderer_recreated'

    def __init__(self, listener_id:str=None, event_type:int=None, is_resistered:bool=False, is_fixed_priority:bool=False, callback=None):
        self.listener_id = listener_id
        self.type = event_type
        self.is_registered = is_registered
        """
        The higher the number, the higher the priority, 0 is for scene graph base priority
        """
        self.is_fixed_priority = is_fixed_priority
        self.node = None
        self.paused = False
        self.enabled = True
        self.on_event = callback
        super().__init__()
        
    def check_available(self):
        return self._on_event != None

"""
Queue for Event Listeners
  - scene_graph_listeners
  - fixed_listeners
"""
class EventListenerList(object):
    def __init__(self):
        self.scene_graph_listeners = []
        self.fixed_listeners = []
        self.gt0Index = 0
        super().__init__()

    def size(self):
        return len(self.scene_graph_listeners) + len(self.fixed_listeners)

    def empty(self):
        return len(self.scene_graph_listeners) == 0 and len(self.fixed_listeners) == 0

    
    def push_back(self, listener:EventListener=None):
        if listener.fixed_priority == 0:
            self.scene_graph_listeners.insert(0, listener)
        else:
            self.fixed_listeners.insert(0, listener)

    
    def clear_scene_graph_listeners(self):
        self.scene_graph_listeners.clear()

    def clear_fixed_listeners(self):
        self.clear_fixed_listeners.clear()

    def clear(self):
        self.clear_scene_graph_listeners()
        self.clear_fixed_listeners()


class ListDict(object):
    def __init__(self):
        self._dict = defaultdict()
        super().__init__()
    
    def push(self, key, value):
        v_list = self._dict[key]
        if v_list == None:
            v_list = []
        
        v_list.append(value)
        self._dict[key] = v_list

    
    def push_back(self, key, value):
        v_list = self._dict[key]
        if v_list == None:
            v_list = []
        v_list.insert(0, value)
        self._dict[key] = v_list


    def pop(self, key, index):
        v_list = self._dict[key]
        if v_list == None:
            return None
        return v_list.pop(index)


    def exists(self, value):
        for key in self._dict.keys():
            if value in self._dict[key]:
                return True
        return False
    
    def get(self, key):
        return self._dict[key]
    
    def keys(self):
        return self._dict.keys()

    def remove_key(self, key):
        v_list = self._dict[key]
        if v_list:
            v_list.clear()
        del self._dict[key]

    
    def clear(self):
        for k in self._dict.keys():
            self.remove_key(k)
        self._dict.clear()


class DirtyFlag(IntEnum):
    NONE = 0
    FIXED_PRIORITY = 1 << 0
    SCENE_GRAPH_PRIORITY = 1 << 1
    ALL = FIXED_PRIORITY | SCENE_GRAPH_PRIORITY

    
"""
EventDispatcher
  - to_added_listeners -- list<EventListener>
  - to_removed_listeners -- list<EventListener>
  - listener_dict - defaultdict<listener_id, EventListerList>
  - priority_dirty_flag_dict == defaultdict<listener_id, DirtyFlag>
  - node_listeners_dict -- ListDict<Node, list<EventListeners>>
  - global_z_node_dict -- ListDict<global_z, list<Node>>
  - node_priority_dict -- dict<node, index>
  - dirty_nodes_set -- set(node)
"""
class EventDispatcher(object):
    def __init__(self):
        self.to_added_listeners = []
        self.to_removed_listeners = []

        self.listener_dict = defaultdict()
        self.priority_dirty_flag_dict = defaultdict()

        self.node_listeners_dict = ListDict()
        self.global_z_node_dict = ListDict()

        self.node_priority_dict = defaultdict()
        self.node_priority_index = 0
        self.dirty_nodes_set = set()

        self.internal_custom_listener_ids = []
        self.internal_custom_listener_ids.append(EventListener.EVENT_COME_TO_FOREGROUND)
        self.internal_custom_listener_ids.append(EventListener.EVENT_COME_TO_BACKGROUND)
        self.internal_custom_listener_ids.append(EventListener.EVENT_RENDERER_RECREATED)
        super().__init__()

    def visit_target(self, node:Node=None, is_root_node:bool=None):
        check_none(node)
        check_none(is_root_node)

        i = 0
        children = node.children
        children_count = len(children)

        if children_count > 0:
            child = None
            for k in children.keys():
                child = children[k]
                if child and child.local_z < 0:
                    visit_target(child, False)
                else:
                    break
            
            if self.node_listeners_dict.exists(node):
                self.global_z_node_dict.push_back(node.global_z, node) 

            for k in children.keys():
                child = children[k]
                if child:
                    visit_target(child, False)
        
        else:
            if self.node_listeners_dict.exists(node):
                self.global_z_node_dict.push_back(node.global_z, node)  
        
        if is_root_node:
            global_z_list = []
            for k in self.global_z_node_dict.keys():
                global_z_list.append(k)
            
            global_z_list = sorted(global_z_list)

            for z in global_z_list:
                for n in self.global_z_node_dict.get[z]:
                    self.node_priority_index += 1
                    self.node_priority_dict[n] = self.node_priority_index

            self.global_z_node_dict.clear()


    def pause_event_listeners_for_target(self, target:Node=None, recursive:bool=False):
        check_none(target)
        listeners = self.node_listeners_dict.get(target)
        for l in listeners:
            l.paused = True

        for l in self.to_added_listeners:
            if l.node == target:
                l.paused = True
        
        if recursive:
            children = target.children
            for child in children:
                self.pause_event_listeners_for_target(child, True)

    
    def resume_event_listeners_for_target(self, target:Node=None, recursive:bool=False):
        check_none(target)
        listeners = self.node_listeners_dict.get(target)
        for l in listeners:
            l.paused = False

        for l in self.to_added_listeners:
            if l.node == target:
                l.paused = False
        
        if recursive:
            children = target.children
            for child in children:
                self.resume_event_listeners_for_target(child, True)


    # TODO - implement
    def remove_event_listener(self, listener:EventListener=None):
        check_none(listener)
        if listener in self.to_removed_listeners:
            return
        
        is_found = False




    def remove_event_listeners_for_target(self, target:Node=None, recursive:bool=False):
        check_none(target)
        del self.node_priority_dict[target]
        self.dirty_nodes_set.remove(target)

        listeners = self.node_listeners_dict.get(target)
        for l in listeners:
            self.remove_event_listener(l)

        for to_add_listener in self.to_add_listeners:
            if to_add_listener.node == target:
                to_add_listener.node = None
                to_add_listener.registered = False
                self.to_add_listeners.remove(to_add_listener)

        if recursive:
            for child in target.children:
                self.remove_event_listeners_for_target(child, True)


    def associate_node_and_event_listener(self, node:Node=None, listener:EventListener=None):
        check_none(node)
        check_none(listener)
        listeners = self.node_listeners_dict.get(node)
        if listeners == None:
            listeners = []
        listeners.insert(0, node)
        self.node_listeners_dict[node] = listeners

    def dissociate_node_and_event_listener(self, node:Node=None, listener:EventListener=None):
        check_none(node)
        check_none(listener)
        listeners = self.node_listeners_dict.get(node)
        if listener in listeners:
            listeners.remove(listener)
        if len(listeners) <= 0:
            self.node_listeners_dict.remove_key(node)



    def add_event_listener(self, listener:EventListener):
        if self.in_dispatch == 0:
            self.force_add_event_listener(listener)
        else:
            self.to_added_listeners.insert(0, listener)

    def force_add_event_listener(self, listener:EventListener):
        listener_id = listener.listener_id
        listeners = self.listener_dict[listener_id]
        if listeners == None:
            listeners = EventListenerList()
            self.listener_dict[listener_id] = listeners
        
        listeners.push_back(listener)

        if listener.fixed_priority == 0:
            self.set_dirty(listener_id, DirtyFlag.SCENE_GRAPH_PRIORITY)
            node = listener.node
            check_none(node)

            self.associate_node_and_event_listener(node, listener)

            if not node.is_running:
                listener.paused = True
        else:
            self.set_dirty(listener_id, DirtyFlag.FIXED_PRIORITY)

    def add_event_listener_with_scene_graph_priority(self, listener:EventListener=None, node:Node=None):
        check(listener and node, 'Invalid parameters')
        check(not listener.is_registered, 'The listener has been registered')

        if not listener.check_available():
            return
        
        listener.node = node
        listener.fixed_priority = 0
        listener.is_registered = True

        self.add_event_listener(listener)

    def add_event_listener_with_fixed_priority(self, listener:EventListener=None, fixed_priority:int=None):
        check_none(listener)
        check(not listener.is_registered, 'The listener has been registered')
        check(fixed_priority != 0, '0 priority is forbidden for fixed priofity since it\'s used for scene graph based priority')

        if not listener.check_available():
            return

        listener.node = None
        listener.fixed_priority = fixed_priority
        listener.is_registered = True
        listener.paused = False

        self.add_event_listener(listener)

    
    def add_custom_event_listener(self, event_name:str=None, callback=None):
        listener = EventListener()
        listener.listener_id = event_name
        listener.on_event = callback
        self.add_event_listener_with_fixed_priority(listener, 1)

    
    def set_priority(self, listener:EventListener=None, fixed_priority:int=None):
        check(listener)
        check(fixed_priority)

        for event_listener_list in self.listener_dict.values():
            fixed_priority_listeners = event_listener_list.fixed_priotiry_listeners
            if listener in fixed_priority_listeners:
                check(listener.node == None, 'Cannot set fixed priority with scene graph based listener')

                if listener.fixed_priority != fixed_priority:
                    listener.fixed_priority = fixed_priority
                    self.set_dirty(listener.listener_id, DirtyFlag.FIXED_PRIORITY)

    def dispatch_event_to_listeners(self, listeners:EventListenerList=None,  on_event=None):
        should_stop_propagation = False
        fixed_priority_listeners = listeners.fixed_listeners
        scene_graph_priority_listeners = listeners.scene_graph_listeners

        i = 0
        if fixed_priority_listeners:
            check(listeners.gt0_index <= len(fixed_priority_listeners), 'Out of range exception')
            if len(fixed_priority_listeners) > 0:
                # priority < 0
                for i in range(listeners.gt0_index):
                    l = fixed_priority_listeners[i]
                    if l.enabled and not l.paused and l.is_registered and on_event(l):
                        should_stop_propagation = True
                        break

        if scene_graph_priority_listeners:
            if not should_stop_propagation:
                # priority == 0, scene graph priority
                for l in scene_graph_priority_listeners:
                    if l.enabled and not l.paused and l.is_registered and on_event(l):
                        should_stop_propagation = True
                        break
        
        if fixed_priority_listeners:
            if not should_stop_propagation:
                # priority > 0
                while i < len(fixed_priority_listeners):
                    l = fixed_priority_listeners[i]
                    i += 1
                    if l.enabled and not l.paused and l.is_registered and on_event(l):
                        should_stop_propagation = True
                        break 
        

        
    def set_dirty_for_node(self, node:Node=None):
        if self.node_listeners_dict.exists(node):
            self.dirty_nodes_set.add(node)
        
        for child in node.children:
            self.set_dirty_for_node(child)


    def set_dirty(self, listener_id:str=None, flag:DirtyFlag=DirtyFlag.NONE):
        dirty_flag = self.priority_dirty_flag_dict[listener_id]
        if dirty_flag == None:
            self.priority_dirty_flag_dict[listener_id] = flag
        else:
            ret = flag | dirty_flag
            self.priority_dirty_flag_dict[listener_id] = ret


    