from time import time
from .base import engine, GameBehavior



class GameFunction:
    def __init__(self, function):
        self._function = function
        self._destroyed = False
        self.start()
        self._running = True

    def wait(seconds):
        start_time = time()
        while (time() - seconds) < start_time:
            yield

    # Wrapper calls for game object handeling
    def add_game_object(self, game_object):
        engine.add_game_object(game_object)

    def remove_game_object(self, game_object):
        engine.remove_game_object(game_object)

    # Calls for function management
    def start(self):
        if self._running:
            return
        if not self._destroyed:
            self._behavior = GameBehavior(self._function)
            engine.start_behavior(self._behavior)

    def pause(self):
        if not self._running:
            return
        if not self._destroyed:
            engine.stop_behavior(self._behavior.ID)

    def stop(self):
        if not self._running:
            return
        if not self._destroyed:
            engine.stop_behavior(self._behavior.ID)
            self._function = None
            self._behavior = None
            self._destroyed = True