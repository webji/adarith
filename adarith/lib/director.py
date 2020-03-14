
import time

import pygame as pg

from .annotation import Singleton
from .core import CGSize, CGColor

from .scheduler import Scheduler
from .actionmanager import ActionManager
from .eventdispatcher import EventDispatcher
from .render import Render
from .node import Node

from .configure import Configure

from .utils import *

from .scene import Scene, TransitionScene

@Singleton
class Director():
    MPF_FILTER = 0.1

    EVENT_BEFORE_SET_NEXT_SCENE = 'director_before_set_next_scene'
    EVENT_AFTER_SET_NEXT_SCENE = 'director_after_set_next_scene'
    EVENT_AFTER_DRAW = 'director_after_draw'
    EVENT_AFTER_VISIT = 'director_after_visit'
    EVENT_BEFORE_UPDATE = 'director_before_update'
    EVENT_AFTER_UPDATE = 'director_after_update'
    EVENT_RESET = 'director_reset'
    EVENT_BEFORE_DRAW = 'director_before_draw'

    def __init__(self):
        self._purge_director_in_next_loop = False
        self._restart_director_in_next_loop = False
        
        

        self._delta_time = 0.0
        self._delta_time_passsed_by_caller = False

        self._animation_interval = 0.0
        self._old_animation_interval = 0.0

        self._display_stats = False
        
        self._accum_dt = 0.0
        self._frame_rate = 0.0

        self._paused = False

        self._total_frames = 0
        self._frames = 0
        self._seconds_per_frame = 1.0
        self._prev_seconds_per_frame = 0.0

        self._running_scene = None

        self._next_scene = None

        self._last_update = 0.0

        self._next_delta_time_zero = False

        self._win_size_in_points = CGSize()

        self._content_scale_factor = 1.0

        

        self._clear_colr = CGColor.clear()

        self._console = None

        self._is_status_label_updated = True

        self._invalid = False

        super().__init__()


    def _set_default(self):
        config = Configure()
        self.fps = config.get_value('adarith.x.fps', Configure.DEFAULT_FPS)
        self._old_animation_interval = self._animation_interval = 1.0/fps




    def init(self, ):
        self._set_default()

        self.clock = pg.time.Clock()

        self._scene_list = []
        self._last_update = self.clock.get_ticks()

        self._notification_node = Node()
        
        # TODO add Console Support
        self._console = None

        self._scheduler = Scheduler()
        self._action_manager = ActionManager()

        self._event_dispatcher = EventDispatcher()
        self._event_before_draw = None
        self._event_after_draw = None
        self._event_after_visit = None
        self._event_before_update = None
        self._event_after_update = None
        self._event_reset_director = None
        self._before_set_next_scene = None
        self._after_set_next_scene = None
        self._render = Render()


    def main_loop(self):
        self.clock.tick(self.fps)
        
        if self._purge_director_in_next_loop:
            self._purge_director_in_next_loop = False
            self.purge_director()
        elif self._restart_director_in_next_loop:
            self._restart_director_in_next_loop = False
            self.restart_director()
        elif not self._invalid:
            self.draw_scene()

        
  
    def main_loop(self, dt):
        self._delta_time = dt
        self._delta_time_passsed_by_caller = True
        self.main_loop()


    def stop_animatioin(self):
        self._invalid = True

    
    def get_window_size(self):
        return self._win_size_in_points

    
    def get_window_size_in_pixels(self):
        return CGSize(self._win_size_in_points.w * self._content_scale_factor, self._win_size_in_points.h * self._content_scale_factor)

    
    def run_with_scene(self, scene:Scene = None):
        check(scene != None, 'Scene should not be null')
        check(self._running_scene == None, '_running_scene should be null')
        self.push_scene(scene)
        self.start_animation()

    def replace_scene(self, scene:Scene = None):
        check(scene != None, 'the scene should not be null')

        if self._running_scene == None:
            self.run_with_scene(scene)
            return
        
        if scene == self._next_scene:
           return

        if self._next_scene:
            if self._next_scene.is_running():
                self._next_scene.on_exit()
            self._next_scene.cleanup()
            self._next_scene = None
        
        index = len(self._scene_list) - 1

        self._send_cleanup_to_scene = True

        self._scene_list[index] = scene
        self._next_scene = scene

    def push_scene(self, scene:Scene=None):
        check(scene != None, 'the scene should not be null')
        self._send_cleanup_to_scene = False
        self._scene_list.append(scene)
        self._next_scene = scene

    
    def pop_scene(self):
        check(self._running_scene != None, 'running scene should not be null')
        self._scene_list.pop()
        c = len(self._scene_list)
        if c == 0:
            self.end()
        else:
            self._send_cleanup_to_scene = True
            self._next_scene = self._scene_list[c-1]


    def calculate_delta_time(self):
        if self._next_delta_time_zero:
            self._delta_time = 0
            self._next_delta_time_zero = False
            self._last_update = self.clock.get_ticks()
        else:
            if not self._delta_time_passsed_by_caller:
                now = self.clock.get_ticks()
                self._delta_time = now - self._last_update
                self._last_update = now
            self._delta_time = max(0, self._delta_time)


    def calculate_MPF(self):
        self._seconds_per_frame = self._delta_time * Director.MPF_FILTER + (1 - Director.MPF_FILTER) * Director.self._prev_seconds_per_frame
        self._prev_seconds_per_frame = self._seconds_per_frame


    def update_frame_rate(self):
        self._frame_rate = 1.0 / self._delta_time


    def set_next_scene(self):
        self._event_dispatcher.dispatch_event(self._before_set_next_scene)

        running_is_transition = isinstance(self._running_scene, TransitionScene)
        new_is_transition = isinstance(self._next_scene, TransitionScene)

        if not new_is_transition:
            if self._running_scene:
                self._running_scene.on_exit_transsition_did_start()
                self._running_scene.on_exit()
            
            if self._send_cleanup_to_scene and self._running_scene:
                self._running_scene.cleanup()
        
        if self._running_scene:
            self._running_scene = None
        
        self._running_scene = self._next_scene
        self._next_scene = None

        if not running_is_transition and self._running_scene:
            self._running_scene.on_enter()
            self._running_scene.on_enter_transition_did_finish()

        self._event_dispatcher.dispatch_event(self._after_set_next_scene)



    def draw_scene(self):
        self._render.begin_frame()
        self.caculate_delta_time()
        events = pg.event.get()

        if not self._paused:
            self._event_dispatcher.dispatch_event(self._event_before_update)
            self._scheduler.update(self._delta_time)
            self._event_dispatcher.dispatch_event(self._event_after_update)
        
        self._render.clear()
        self._event_dispatcher.dispatch_event(self._event_before_draw)
        
        if self._next_scene:
            self.set_next_scene()
        
        if self._running_scene:
            self._render.clear_draw_stats()
            self._render.render_scene(self._running_scene)
            self._event_dispatcher.dispatch_event(self._event_after_visit)

        if self._notification_node:
            # TODO implement visit
            self._notification_node.visit(self._render)
        
        self.update_frame_rate()

        if self._display_stats:
            self.show_status()

        self._render.render()
        self._event_dispatcher.dispatch_event(self._event_after_draw)

        self._total_frames += 1

        pg.display.update()

        self._render.end_frame()

        if self._display_stats:
            self.calculate_MPF()




    """
    Wrapper ot pygame.time.Clock.get_ticks
    Return the milliseconds after pg.int()
    """
    def get_ticks(self):
        return self.clock.get_ticks()

    
    """
    display the FPS using a LabelAtlas
    updates the FPS every frame
    """

    def show_stats(self):
        if self._is_status_label_updated:
            self.create_stats_label()
            self._is_status_label_updated = False

        self._prev_calls = 0
        self._pref_verts = 0

        self._frames += 1
        self._accum_dt += self._delta_time

        if self._display_stats and self._fps_label and self._drawn_batches_label and self._drawn_vertices_label:
            fps_str = f'{self._frames / self._accum_dt} / {self._seconds_per_frame}'
            self._fps_label.set_str(fps_str)

            current_calls = self._render.get_drawn_batches()
            current_verts = self._render.get_draw_vertices()
            if current_calls != self._prev_calls:
                batch_str = f'Batch calls: {current_calls}'
                self._draw_batches_label.set_str(batch_str)
                self._prev_calls = current_calls
            
            if current_verts != self._prev_verts:
                vert_str = f'Verts: {current_verts}'
                self._draw_vertices_label.set_str(vert_str)
                self._prev_verts = current_verts

            self._draw_vertices_label.visit(_render)
            self._draw_batches_label.visit(_render)
            self._fps_label.visit(_render)

