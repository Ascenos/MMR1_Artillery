import random
from tools import vector2

class Wind:

    def __init__(self):
        self.direction = vector2(random.random(), random.random())

    def changeDirection(self):
        self.direction = vector2(random.random(), random.random())