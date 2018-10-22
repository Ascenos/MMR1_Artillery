from engine import *
from .base import engine
from time import time, sleep
import app



class Managed:
    def __init__(self, renderer):
        # Do not start the loop at creation time
        self._updating = False
        # Set needed renderer for engine here
        engine.renderer = renderer

    def start(self):
        self._updating = True

    def stop(self):
        self._updating = False

    def loop(self, **kwargs):
        # TODO make timer configuratable
        # TODO more functionality here
        update_time = kwargs.pop('deltaUpdate', 1/30)

        start_time = time()
        while True:
            # Wait for update
            while not self._updating:
                if self._updating:
                    start_time = time()
                    break
            # Let the engine update
            engine.update()
            # Calculate time between advances
            end_time = time()
            computation_time = end_time - start_time
            if computation_time > update_time:
                # TODO logging warning low framerate
                raise RuntimeError('Framerate too low.')
            wait_time = update_time - computation_time
            # Adjust expected start_time
            start_time = end_time + wait_time
            # Wait for next step
            sleep(wait_time)
            # TODO remove log
            print('Update')

# Start main function and add to engine.
app.main_function()

# Provide a simple api to allow easier calls
_temp_managed = Managed()
start = _temp_managed.start
stop  = _temp_managed.stop
loop  = _temp_managed.loop
