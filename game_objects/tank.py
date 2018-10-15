from engine import *



class Tank(InputObject):
    def on_start(self):
        self._start_behavior(self.update_function_cr)

    def update_function_cr(self):
        # Do shit
        while True:
            yield
