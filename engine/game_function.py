from time import time
from .base import engine, GameBehavior



class GameFunction:
    def __init__(self):
        self._function = self.function
        self._destroyed = False
        self._running = False
        self.start()

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
        if self._destroyed:
            return
        if self._running:
            return
        self._behavior = GameBehavior(self._function)
        engine.start_behavior(self._behavior)
        self._running = True

    def pause(self):
        if self._destroyed:
            return
        if not self._running:
            return
        engine.stop_behavior(self._behavior.ID)
        self._running = False

    def stop(self):
        if self._destroyed:
            return
        if not self._running:
            return
        engine.stop_behavior(self._behavior.ID)
        self._function = None
        self._behavior = None
        self._destroyed = True
