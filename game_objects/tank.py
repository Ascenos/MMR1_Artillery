from engine import *
from utils.slope_acceleration import (
    slope_x_acceleration,
    slope_downwards_acceleration,
)



class Tank(InputObject):
    def __init__(self, x):
        super().__init__()
        self._ACCELERATION = 5
        self._MAX_SPEED = 20
        self._GRAVITY = 10
        self._FRICTION = 2
        self.x = x
        self.speed = 0
        self.old_speed = 0

    def on_start(self):
        self._start_behavior(self.update_function_cr)

    def update_function_cr(self):
        while True:
            # Walk through input buffer
            for input in self.get_input():
                # TODO process inputs here
                pass
            yield

    def _max_speed(self):
        return self.speed >= self._MAX_SPEED

    def accelerate(self, right):
        """
        Accelerate to the given direction
        """
        if not self._max_speed(self):
            self.speed += (self._ACCELERATION if right else -self._ACCELERATION)
                + slope_downwards_acceleration(y1, y2, x, self._GRAVITY)
            if self._max_speed(self):
                self.speed = self._MAX_SPEED

    def move(self):
        self.x += slope_x_acceleration(self.speed)
        self.speed -= self._FRICTION
