import math

class Vector(object):
    """
    A vector utility class.

    Will be deprecated by Vector2 and Vector3 classes (soon enough)
    """
    def __init__(self, *args):
        self.values = (0, 0) if len(args) == 0 else args

    @property
    def magnitude(self):
        """
        Returns the magnitude of the vector
        """
        return math.sqrt(sum(comp**2 for comp in self))

    @property
    def argument(self):
        """
        Returns the argument of the vector (angle clockwise from +y)
        """
        arg_in_rad = math.acos(Vector(0,1)*self/self.norm())
        arg_in_deg = math.degrees(arg_in_rad)
        return (arg_in_deg) if self.values[0] >= 0 else (360 - arg_in_deg)

    @property
    def normalized(self):
        """
        Returns the normalized unit vector
        """
        magnitude = self.magnitude
        normed = (comp / magnitude for comp in self)
        return Vector(*normed)

    def rotated(self, degrees):
        """
        Rotate this vector. Assumes this is a 2D vector and
        rotates by the passed value in degrees.
        """
        if isinstance(degrees, (int, float)):
            theta = math.radians(degrees)
            # Just applying the 2D rotation matrix
            dc, ds = math.cos(theta), math.sin(theta)
            x, y = self.values
            new_x, new_y = dc*x - ds*y, ds*x + dc*y
            return Vector(new_x, new_y)

    def matrix_mult(self, matrix):
        """
        Multiply this vector by a matrix.  Assuming matrix is a list of lists.

        Example:
        mat = [[1, 2, 3], [-1, 0, 1], [3, 4, 5]]
        Vector(1, 2, 3).matrix_mult(mat) ->  (14, 2, 26)
        """
        if not all(len(row) == len(self) for row in matrix):
            raise ValueError('Matrix must match vector dimensions')
        product = (Vector(*row) * self for row in matrix)
        return Vector(*product)

    def inner(self, other):
        """
        Returns the dot product (inner product) of self and other vector
        """
        return sum(a * b for a, b in zip(self, other))

    def __mul__(self, other):
        """
        Returns the dot product of self and other if multiplied
        by another Vector. If multiplied by an int or float,
        multiplies each component by other.
        """
        if isinstance(other, Vector):
            return self.inner(other)
        elif isinstance(other, (int, float)):
            product = (a * other for a in self)
            return Vector(*product)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, (int, float)):
            divided = (a / other for a in self)
            return Vector(*divided)

    def __add__(self, other):
        added = (a + b for a, b in zip(self, other))
        return Vector(*added)

    def __sub__(self, other):
        subbed = (a - b for a, b in zip(self, other))
        return Vector(*subbed)

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __repr__(self):
        return 'Vector' + str(self.values)