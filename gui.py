import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QDesktopWidget, QPushButton, QComboBox, QVBoxLayout, QFrame
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import logging

from tank import TanksMain
from guiUtility import VMenu

menuStyleSheet = \
"""
TanksWindow {
    background-color: #2096f0;
}
QLabel {
    background-color: rgba(64, 64, 64, 128)
}
VMenuElement {
    background-color: #aaa;
    border: 5px outset #777;
    color: black;
    font: 40px \"Montserrat\";
}
VMenuElement:hover {
    background-color: #a9a9a9;
    border-color: #696969;
}
VMenuElement:pressed {
    background-color: #999;
    border-color: #888;
    border-style: inset;
}
VMenu {
    background-color: #ccc;
    border: 5px double #aaa;
}
"""

class TanksWindow(QMainWindow):
    def __init__(self, resolution = (1920, 1080), fullscreen = False):
        super().__init__()
        self.setStyleSheet(menuStyleSheet)
        self.game_label = QLabel(self)
        self.game_paused_label = QLabel(self.game_label)
        self.logger = logging.getLogger(__name__)
        ### Generate GUIs
        self.generate_main_menu()
        self.generate_game_menu()
        # Set game status
        self.close_game()
        # Show
        if fullscreen:
            self.showFullScreen()
            self.game_size = (self.width(), self.height())
        else:
            self.show()
            self.resize(*resolution)
            self.game_size = resolution
        ### Resize GUIs
        self.game_label.resize(*self.game_size)
        self.game_paused_label.resize(*self.game_size)
        self.resize_main_menu()
        self.resize_game_menu()

        ### Start main-loop
        def main_loop():
            self.logger.debug('Calling "main_loop"')
            if self.game != None:
                self.game.generate_impact(4000, 400)
                self.terrain_drawn = False
                self.show_game()
            
        self.timer = QTimer()
        self.timer.timeout.connect(main_loop)
        self.timer.start(3000)

    def reset_game_status(self):
        # Logging
        self.logger.debug('Calling "reset_game_status"')
        # Background
        self.background = None
        # Terrain
        self.terrain_drawn = False
        self.terrain = None

    def generate_main_menu(self):
        # Logging
        self.logger.debug("Generating main menu.")
        # Function
        self.main_menu = VMenu(self)
        self.main_menu.add_element(2, 1, "New Game", self.start_game)
        self.main_menu.add_element(2, 1, "Profiles")
        self.main_menu.add_element(2, 1, "Settings")
        self.main_menu.add_element(1, 1, "Credits")
        self.main_menu.add_element(1, 0, "Exit", self.close)

    def resize_main_menu(self):
        # Logging
        self.logger.debug("Resizing main menu.")
        # Function
        self.main_menu.resize(self.width()//3, self.height()//1.1)
        self.main_menu.move((self.width()-self.main_menu.width())//2, (self.height()-self.main_menu.height())//2)

    def generate_game_menu(self):
        # Logging
        self.logger.debug("Generating game menu.")
        # Function
        self.game_menu = VMenu(self.game_paused_label, 1)
        self.game_menu.add_element(4, 2, "Continue", self.continue_game)
        self.game_menu.add_element(4, 2, "Settings")
        self.game_menu.add_element(4, 2, "Main Menu", self.close_game)
        self.game_menu.add_element(4, 2, "Exit", self.close)

    def resize_game_menu(self):
        # Logging
        self.logger.debug("Resizing game menu.")
        # Function
        self.game_menu.resize(self.width()//3, self.height()//1.1)
        self.game_menu.move((self.width()-self.game_menu.width())//2, (self.height()-self.game_menu.height())//2)

    def show_menu(self):
        # Logging
        self.logger.debug('Calling "show_menu"')
        if self.game == None:
            # Logging
            self.logger.debug(">>Showing main menu.")
            # Hide game_label
            self.game_label.hide()
            self.main_menu.show()
        else:
            # Logging
            self.logger.debug(">>Showing game menu.")
            self.pause_game()
            self.game_menu.show()
                 
    def generate_game(self):
        # Logging
        self.logger.debug('Calling "generate_game"')
        self.game = TanksMain(players = 2, bots = 0)
        
    def start_game(self):
        # Logging
        self.logger.debug('Calling "start_game"')
        self.main_menu.hide()
        if self.game != None:
            self.show_game()
        else:
            self.generate_game()
            self.show_game()

    def pause_game(self):
        # Logging
        self.logger.debug('Calling "pause_game"')
        self.game_paused_label.show()

    def continue_game(self):
        # Logging
        self.logger.debug('Calling "continue_game"')
        self.game_paused_label.hide()

    def close_game(self):
        # Logging
        self.logger.debug('Calling "close_game"')
        self.game = None
        self.reset_game_status()
        self.game_paused_label.hide()
        self.show_menu()

    def show_game(self):
        # Logging
        self.logger.debug('Calling "show game"')
        self.game_label.show()
        self.game_label.resize(*self.game_size)
        ### Background
        if self.background == None:
            self.background = QImage(*self.game_size, QImage.Format_RGB888)
            gradient = QRadialGradient(self.game_size[0], 0, self.game_size[0])
            gradient.setColorAt(0, QColor(255, 255, 0))
            gradient.setColorAt(0.1, QColor(255, 200, 0))
            gradient.setColorAt(0.11, QColor(255, 255, 160))
            gradient.setColorAt(0.2, QColor(200, 255, 240))
            gradient.setColorAt(1, QColor(32, 150, 240))
            painter = QPainter(self.background)
            painter.fillRect(QRect(0, 0, *self.game_size), gradient)
        ### Terrain
        if not self.terrain_drawn:
            self.draw_terrain()
        ### Combining images
        # Copy background
        picture = self.background.copy()
        painter = QPainter(picture)
        # Draw terrain
        painter.drawImage(self.terrain[1], self.terrain[2], self.terrain[0])
        # Draw water
        water = QImage(self.game_size[0], self.game_size[1]//9, QImage.Format_RGBA8888)
        water.fill(QColor(0, 0, 32, 128))
        painter.drawImage(0, self.game_size[1]//9*8, water)
        self.game_label.setPixmap(QPixmap.fromImage(picture))

    def draw_terrain(self):
        # Logging
        self.logger.debug('Calling "draw_terrain"')
        ##########################################################
        ### Terrain-colors
        color_ground1 = np.asarray((136, 48, 0, 255), dtype = np.uint8)
        color_ground2 = np.asarray((120, 40, 0, 255), dtype = np.uint8)
        color_ground3 = np.asarray((96, 32, 0, 255), dtype = np.uint8)
        color_ground4 = np.asarray((80, 24, 0, 255), dtype = np.uint8)
        color_border = color_ground3
        ##########################################################
        if True:
            # Logging
            self.logger.debug('Calling "self.game.relative_terrain"')
            ### Terrain bit-values
            terrain_values = self.game.relative_terrain(self.game_size)
            ### Divide into islands
            # Logging
            self.logger.debug('Dividing into islands.')
            # Map starts either with a sea or land
            sea = terrain_values[0] <= 0
            borders = [] if sea else [0]
            for i in range(self.game_size[0]):
                # Add border if terrain changes from sea to land
                if sea and terrain_values[i] > 0:
                    borders.append(i)
                    sea = False
                # Add border if terrain changes from land to sea
                if not sea and terrain_values[i] <= 0:
                    borders.append(i)
                    sea = True
            # Add border if terrain ends with land
            if not sea: borders.append(self.game_size[0]-1)
            ##########################################################
            # Logging
            self.logger.debug('Drawing islands')
            ### Draw islands [Current Built: 1 Island]
            terrain_values = terrain_values[borders[0]:borders[1]]
            # Length and position of island
            length_x, length_y = borders[1] - borders[0], max(terrain_values)
            position_x, position_y = borders[0], self.game_size[1] - length_y
            ##########################################################
            ### Terrain values to 8 bit RGBA-values
            ## Repeating height:
            # ...
            # (1, 1, 1, 1), ...
            # (0, 0, 0, 0), (0, 0, 0, 0), ...
            number = np.repeat(np.arange(length_y-1, -1, -1, dtype = np.int16), length_x*4)
            ## Repeating terrain values:
            # ...
            # (value[0], value[0], value[0], value[0]), ...
            # (value[0], value[0], value[0], value[0]), (value[1], value[1], value[1], value[1]), ...
            value = np.repeat(np.tile(terrain_values, length_y), 4)
            # Terrain rgba values:
            terrain_rgba = np.zeros(length_x*length_y*4, dtype = np.uint8)
            # Mask for maincolor
            np.putmask(terrain_rgba, value > number, np.tile(color_ground1, length_x*length_y))
            # Masks for other colors 
            np.putmask(terrain_rgba, value*1.25-max(value)//2 > number, np.tile(color_ground2, length_x*length_y))
            np.putmask(terrain_rgba, value*1.5-max(value) > number, np.tile(color_ground3, length_x*length_y))
            np.putmask(terrain_rgba, value*1.75-int(max(value)*1.5) > number, np.tile(color_ground4, length_x*length_y))
            # Generate Image
            self.terrain = QImage(terrain_rgba, length_x, length_y, QImage.Format_RGBA8888), position_x, position_y
            ##########################################################
        self.terrain_drawn = True
        # Logging
        self.logger.debug('Finished "draw_terrain"')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.show_menu()
        if e.key() == Qt.Key_Control:
            #self.close()
            pass

    def close(self):
        super().close()
        self.timer.deleteLater()

    """
        # Draw Tanks4
        tank = QPixmap("Tanks_x2.png")
        painter.drawPixmap(QRectF(round(self.position/self.relation)- 50, self.resolution[1] - round(self.main.terrain[self.position]/self.relation) - 100, 100, 100), tank, QRectF(0, 0, 100, 100))
    """
        


if __name__ == "__main__":
    ##########################################################
    ### Logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    ##########################################################
    app = QApplication(sys.argv)
    main = TanksWindow(resolution = (1600, 900), fullscreen = True)
    sys.exit(app.exec_())
