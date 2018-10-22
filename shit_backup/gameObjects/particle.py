from tools.vector2 import Vector2

class Particle:

    def __init__(self, positionX, positionY, width, height, speedX, speedY, color):
        self.position = Vector2(positionX, positionY)
        self.size = Vector2(width, height)
        self.speed = Vector2(speedX, speedY)
        self.color = color

    def move(self):
        self.position += self.speed * 0.4
