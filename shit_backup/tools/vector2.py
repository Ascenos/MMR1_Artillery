import math

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)
        return self.x * other.x + self.y * other.y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise Exception("Index out of range")

    def __iter__(self):
        yield self.x
        yield self.y

    def __str__(self):
        return "({} | {})".format(self.x, self.y)

    def __round__(self, n=0):
        return Vector2(round(self.x, n), round(self.y, n))

    def copy(self):
        return Vector2(self.x, self.y)

    def length(self):
        return (self.x**2 + self.y**2)**0.5

    def normalized(self):
        length = self.length()
        return Vector2(self.x / length, self.y / length)

    def normalize(self):
        length = self.length()
        self.x /= length
        self.y /= length

    def rotated(self, degree):
        rad = getRadian(degree)
        s, c = math.sin(rad), math.cos(rad)
        return Vector2(round(self.x*c - self.y*s, 12), round(self.x*s + self.y*c, 12))

    def rotate(self, degree):
        rad = getRadian(degree)
        s, c = math.sin(rad), math.cos(rad)
        x, y = round(self.x*c - self.y*s, 12), round(self.x*s + self.y*c, 12)
        self.x, self.y = x, y


def getRadian(degree):
    return degree/180*math.pi

if __name__ == "__main__":
    pass
