from time import time
from .base import engine, GameBehavior



# Implementing game object
class GameObject:
    def __new__(cls, *args, **kwargs):
        """
        Creates the object and adds it into the engines game_objects list
        """
        game_object = super().__new__(cls)
        # Activate item
        game_object._active = True
        # Don't set it visible though
        game_object._visible = False
        # Starting class has no behaviors
        game_object._behaviors = []
        # Create a list to hold grouped game objects
        gema_object._sub_objects = []
        # Add object to the engine
        engine.add_game_object(game_object)
        return game_object

    @property
    def ACTIVE(self):
        return self._active

    @property
    def VISIBLE(self):
        return self._visible

    def on_start(self):
        """
        Function that gets called on start.
        """
        pass

    def on_end(self):
        """
        Function that gets called on end of the lifetime
        """
        pass

    def on_destroy(self):
        """
        Function that gets called on destroy
        """
        self._stop_all_behaviors()
        for sub_object in self._sub_objects:
            sub_object.on_end()

    def render(self, frame):
        """
        Renders the picture on the passed frame.
        """
        pass

    # Helper function to be able to wait (non blocking)
    # Use this when writing coroutines to change
    def wait(seconds):
        start_time = time()
        while (time() - seconds) < start_time:
            yield

    # Here come calls to the engine for convinience sake
    def _start_behavior(self, function):
        behavior = GameBehavior(function)
        self._behaviors.append(behavior)
        engine.start_behavior(behavior)

    def _stop_behavior(self, function):
        for behavior in self._behavior:
            if behavior.base_function == function:
                engine.stop_behavior(behavior)
                self._behavior.remove(behavior)
                return

    def _destroy_self(self):
        engine.remove_game_object(self)

    def _add_sub_object(self, sub_object):
        self._sub_objects.append(sub_object)
        return len(self._sub_objects) - 1

    def _remove_sub_object(self, sub_object_id):
        del self._sub_objects[sub_object_id]

    def _stop_all_behaviors(self):
        for behavior in self._behavior:
            engine.stop_behavior(behavior.ID)

    def _search_game_objects(self, strict_object_type, filter=None):
        """
        Uses the search function to get a specific loaded game object
        """
        return engine.search_for_objects(strict_object_type)
