
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
        self.id = None
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

    
    def clear(self):
        for k in self._dict.keys():
            v_list = self._dict[k]
            v_list.clear()
            del self._dict[k]
        self._dict.clear()


    
"""
EventDispatcher
  - to_added_listeners -- list<EventListener>
  - to_removed_listeners -- list<EventListener>
  - node_listeners_dict -- ListDict<Node, list<EventListeners>>
  - global_z_node_dict -- ListDict<global_z, list<Node>>
  - node_priority_dict -- dict<node, index>
  - dirty_nodes_set -- set(node)
"""
class EventDispatcher(object):
    def __init__(self):
        self.to_added_listeners = []
        self.to_removed_listeners = []

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

    def remove_event_listeners_for_target(self, target:Node=None, recursive:bool=False):
        check_none(target)
        del self.node_priority_dict[target]
        

        

    