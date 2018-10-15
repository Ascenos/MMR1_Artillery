from time import time
from .base import engine, GameBehavior



# TODO MASSIVE WORK HERE
# Implementing game object
class GameObject:
    def __new__(cls, *args, **kwargs):
        """
        Creates the object and adds it into the engines game_objects list
        """
        game_object = super().__new__(cls, *args, **kwargs)
        engine.add_game_object(game_object)
        return game_object

    def __init__(self):
        # Activate item
        self._active = True
        # Don't set it visible though
        self._visible = False
        # Starting class has no behaviours
        self._behaviors = []

    @property
    def ACTIVE(self):
        return self._active

    @property
    def VISIBLE(self):
        return self._visible

    # Helper function to be able to wait (non blocking)
    # Use this when writing coroutines to change
    def wait(seconds):
        start_time = time()
        while (time() - seconds) < start_time:
            yield

    # Here come calls to the engine for convinience sake
    def _start_behavior(self, function):
        behavior = GameBehavior(function, self)
        self._behaviors.append(behavior)
        engine.add_coroutine(behavior)

    def _stop_behavior(self, function):
        for behavior in self._behavior:
            if behavior.base_function == function
                engine.stop_coroutine(behavior.ID)
                self._behavior.remove(behavior)
                return

    def _stop_all_behaviors(self):
        for behavior in self._behavior:
            engine.stop_coroutine(behavior.ID)

    def _get_game_objects(self, strict_object_type, filter=None):
        """
        Uses the search function to get a specific loaded game object
        """
        return engine.search_for_objects(strict_object_type)