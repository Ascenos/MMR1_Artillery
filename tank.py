import numpy as np
from legendrePolynom import legendre_polynom

from tankUtility import *

class TanksMain():
    def __init__(self, players = 2, bots = 0):
        ### Optimization resolutions
        ## 16x9:
        # WXGA is included in QHD
        #QHD:   2560x1440, 320*8x180*8
        #FHD:   1920x1080, 320*6x180*6
        #HD+:   1600x900, 320*5x180*5
        #WXGA:1280x720, 320*4x180*4
        ## 4x3:
        #
        ### Constants
        # 320*6*5*2, 180*6*5*2
        self.__players = players
        self.__bots = bots
        self.__width, self.__height = 19200, 10800
        self.generate_terrain()

    def generate_terrain(self):
        # Points from which a polynom is generated.
        x_points = np.linspace(int(0.1*self.__width), int(0.9*self.__width)-1, 11)
        y_points = np.asarray([0, 0.2*self.__height, 0.22*self.__height, 0.26*self.__height, 0.28*self.__height, 0.24*self.__height, 0.20*self.__height, 0.22*self.__height, 0.26*self.__height, 0.2*self.__height, 0])
        # Actual values
        x_values = np.arange(0, self.__width, 1, dtype = np.int16)
        y_values = legendre_polynom(x_points, y_points)(np.arange(0, self.__width, 1, dtype = np.int16))
        # Mask for values outside of the polynom
        np.putmask(y_values, np.logical_or(x_values < 0.1*self.__width, x_values > 0.9*self.__width), 0)
        self.__terrain = y_values.astype(dtype = np.int32)

    def generate_tanks(self):
        pass

    def generate_impact(self, x, size):
        width_factor = 4
        impact = (((np.cos(np.arange(1, size*width_factor*2, 1, dtype = np.float64) / size / width_factor * np.pi)) - 1)*size/2).astype(dtype = np.int32)
        self.impact.append([max(x-size*width_factor, 0), min(x+size*width_factor, self.__width)])
        self.terrain[max(x-size*width_factor+1, 0):min(x+size*width_factor, self.__width)] += impact

    def relative_terrain(self, size):
        """
        Return the amount of terrain values needed to be compressed in order the obtain the wanted pixel amount.
        """
        terrain = np.zeros(size[0], dtype = np.int32)
        size_factor = self.__width // size[0]
        for i in range(size_factor):
            terrain += self.terrain[np.arange(i, self.__width, size_factor)]
        return terrain // size_factor**2

    @property
    def terrain(self):
        return self.__terrain

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self._height

if __name__ == "__main__":
    main = TanksMain()
    main.generate_impact(6000, 10)
