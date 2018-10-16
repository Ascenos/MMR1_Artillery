from engine import *
from .base import engine
from time import time, sleep
from game_functions.main import MainGameFunction



# TODO implement singleton (?)
class Managed:
    def __init__(self):
        self._updating = False

    def start(self):
        self._updating = True

    def stop(self):
        self._updating = False

    def loop(self, **kwargs):
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
            print('Update')

# Start main function and add to engine.
# Main functions need to be this specific class
MainGameFunction()

# Provide a simple api to allow easier calls
_temp_managed = Managed()
start = _temp_managed.start
stop  = _temp_managed.stop
loop  = _temp_managed.loop
