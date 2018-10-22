from gameObjects.particle import Particle
from tools.vector2 import Vector2

class Projectile(Particle):

    def __init__(self, positionX, positionY, width, height, speedX, speedY, color):
        super(Projectile, self).__init__(positionX, positionY, width, height, speedX, speedY, color)

    def move(self):
        self.position += self.speed * 0.4
        self.speed += Vector2(0,0.5)
