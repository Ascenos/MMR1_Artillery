import sys, random, math
from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QImage, QIcon, QBrush, QPen, QFont
import logging

from tools.vector2 import Vector2
from gameObjects import Particle, Tank, Projectile, Player, Terrain
from gui.vMenu import VMenu

import numpy as np


menuStyleSheet = \
"""
Artillery {
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

class Artillery(QMainWindow):
    """
        Die Artillery Klasse beschreibt das Hauptfenster der gesamten Anwendung.
        In der Anwendung befindet sich ein QFrame, in welchem und auf
        welchem das eigentliche Spiel stattfindent.
    """
    def __init__(self, resolution = (1600, 900), fullscreen = False):
        """
            Initiert alle nötigen Widgets der Anwendung und Eigenschaften
            des Fensters.
        """
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
            self.setWindowTitle("Artillery")
            self.show()
            self.resize(*resolution)
            self.center()
            self.game_size = resolution
        ### Resize GUIs
        self.game_label.resize(*self.game_size)
        self.game_paused_label.resize(*self.game_size)
        self.resize_main_menu()
        self.resize_game_menu()

    def center(self):
        """
        Centers the windowed widget.
        """
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width()-self.width())/2, (screen.height()-self.height())/2)

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
        width, height = self.width(), self.height()
        if width*9 == height*16:
            self.logger.debug('Window size fits 16x9')
            self.game = Game(self, width, height, 3)
            self.game.resize(width, height)
        elif width*9 < height*16:
            self.logger.debug('Window width smaller than 16x9')
            self.game = Game(self, width, int(width/16*9), 3)
            self.game.resize(width, int(width/16*9))
            self.game.move(0, (height-int(width/16*9))//2)
            print("test")
        else:
            self.logger.debug('Window height smaller than 16x9')
            self.game = Game(self, height/9*16, height, 3)
            self.game.resize(height/9*16, height)
            self.game.move((width-self.game.width())//2, 0)

    def show_game(self):
        # Logging
        self.logger.debug('Calling "show_game"')
        self.game.show()
        # Das Spiel wird hier gestartet
        self.game.start()

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
        self.game_paused_label.hide()
        self.show_menu()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.show_menu()
        if e.key() == Qt.Key_Control:
            #self.close()
            pass



class Game(QLabel):
    """
        Die Game Klasse beschreibt das tatsächliche Spiel. Sie besitzt Listen
        mit Spielobjekten, einen Timer, einen Painter, berechnet den Verlauf
        des Spiels und gibt ihn wieder.
    """

    def __init__(self, parent, width, height, playerCount):
        """ Initierung einfacher Variablen."""
        super().__init__(parent)

        self.width = width
        self.height = height
        self.playerCount = playerCount
        self.currentPlayerNum = 0                                      # Der erste Spieler ist der erste in der Liste
        self.speed = 17                                             # Das Bild wird alle so viele MS erneuert

        self.initGame()

    def initGame(self):
        """ Initierung der Spielobjekte, des Timers und anderer wichtiger
            Elemente.
        """
        self.setFocusPolicy(Qt.StrongFocus)                         # Dieser Befehl ist sehr wichtig, damit das QFrame
                                                                    # für das KeyPressEvent hören kann
        self.terrain = Terrain(self.width, self.height)
        self.terrain.generateByFourierSynthesis()
        self.terrain.generateQImage()
        self.particles = []
        self.projectiles = []
        self.players = []
        players = [("Amadeus", Qt.red), ("Jannik", Qt.green), ("Mario", Qt.blue)]  # diese Liste sollte später in einem Auswahlfenster erstellt werden
        for num, (name, color) in enumerate(players):
            tank = Tank((num+1)*self.width/(len(players)+1),500,self.terrain,2,color)
            self.players.append(Player(name, tank))
        self.timer = QBasicTimer()                              # Timer des Spiels

    def start(self):
        """ Start des Spiels."""
        self.timer.start(self.speed, self)                          # Starten des Timers

    def paintEvent(self, QPaintEvent):
        """ Generiert einen Painter und gibt ihm die Anweisung das Spiel
            zu zeichnen.
        """

        painter = QPainter(self)
        self.drawGame(painter)                                      # Zeichnen der Spielelemente
        painter.end()

    def drawGame(self, painter):
        """ Zeichnet alle Spielgegenstände."""
        self.drawBackground(painter)
        self.terrain.drawImage(painter)
        self.drawStatus(painter)
        self.drawParticles(painter)
        self.drawProjectile(painter)
        self.drawTanks(painter)


    def drawBackground(self, painter):
        """ Zeichnet den Hintergrund."""
        painter.fillRect(0,0, self.width, self.height, QColor(200,220,255))

    def drawParticles(self, painter):
        """ Anweisung zum Zeichnen von Rechteckigen Partikeln."""
        for particle in self.particles:
            painter.fillRect(particle.position.x, particle.position.y, particle.size.x, particle.size.y, particle.color)

    def drawTanks(self, painter):
        """ Anweisung zum Zeichnen von Panzern."""
        for player in self.players:
            # Zeichnet den Körper
            if player.inGame:
                tank = player.tank
                brush = QBrush(tank.body.color)
                pen = QPen(tank.body.color, 1)
                painter.setBrush(brush)
                painter.setPen(pen)
                painter.drawEllipse(tank.positionX - tank.radius/4, tank.positionY - tank.radius/4, tank.radius/2, tank.radius/2)

                # Der Teil hier ist sehr wichtig für die Rotation des Laufs
                # Zuerst wird der Ursprung des Koordinatensystems auf die Mitte der Südlichen Kante des Laufs positioniert
                painter.translate(QPointF(tank.rifleX + (tank.rifleThickness/2) , tank.rifleY + tank.rifleLength))
                # Dann wird das Koordinatensystem um die Neigung des Laufs gedreht
                painter.rotate(tank.rifleDegree-90)
                # Dann wird der Lauf in diesem Koordinatensystem gezeichnet
                # Der Ursprung befindet sich ja in der Mitte der gewünschten Position und dieser kleine Teil wird hier
                # noch berücksichtigt und angepasst
                painter.fillRect( -(tank.rifleThickness/2) , -tank.rifleLength, tank.rifle.size.x, tank.rifle.size.y,
                                 tank.rifle.color)
                # Nach der Zeichnung wird der Painter wieder zurückgesetzt auf das normale Koordinatensystem
                painter.rotate(-tank.rifleDegree+90)
                painter.translate(QPointF(-(tank.rifleX + (tank.rifleThickness/2)),-(tank.rifleY + tank.rifleLength)))

                pen = QPen(Qt.black, 1)
                painter.setPen(pen)
                painter.drawPoint(tank.positionX, tank.positionY)
                #powerBar
                if tank.shooting:
                    powerBarWidth = self.width/30
                    powerBarHeight = self.height/40
                    painter.fillRect(tank.positionX-powerBarWidth/2, tank.positionY-100,
                                     powerBarWidth*tank.powerBarCurrent/tank.powerBarMax, powerBarHeight, Qt.red)

    def drawStatus(self, painter):
        painter.setFont(QFont("Times", 30))
        painter.drawText(10, 50, "%s ist am Zug!" % self.currentPlayer.name)

    def drawProjectile(self, painter):
        """ Zeichnet alle Projektiele."""
        for projectile in self.projectiles:
            painter.fillRect(projectile.position.x, projectile.position.y, projectile.size.x, projectile.size.y, projectile.color)

    def timerEvent(self, QTimerEvent):
        """ Die Haupt-Spiel-Schleife (Main Game Loop)."""
        for particle in self.particles:
            particle.move()
        for player in self.players:
            player.tank.update()
        for projectile in self.projectiles:
            projectile.move()
        self.update()
# Zeichnet das Bild neu


    def keyPressEvent(self, QKeyEvent):
        """ Der Eventhandler für gedrückte Tasten"""
        key = QKeyEvent.key()

        if key == Qt.Key_Left:
            self.currentPlayer.tank.movingLeft = True
        elif key == Qt.Key_Right:
            self.currentPlayer.tank.movingRight = True
        elif key == Qt.Key_Up:
            self.currentPlayer.tank.movingRifleRight = True
        elif key == Qt.Key_Down:
            self.currentPlayer.tank.movingRifleLeft = True

    def keyReleaseEvent(self, QKeyEvent):
        """ Der Eventhandler für losgelassene Tasten"""
        key = QKeyEvent.key()

        if key == Qt.Key_Left:
            self.currentPlayer.tank.movingLeft = False
        elif key == Qt.Key_Right:
            self.currentPlayer.tank.movingRight = False
        elif key == Qt.Key_Up:
            self.currentPlayer.tank.movingRifleRight = False
        elif key == Qt.Key_Down:
            self.currentPlayer.tank.movingRifleLeft = False
        elif key == Qt.Key_Space:
            if self.currentPlayer.tank.shooting:
                self.shoot()
            else:
                self.currentPlayer.tank.shooting = True

    def shoot(self):
        """ Schießt ein Projektil aus dem Lauf des aktuellen Panzers"""
        self.projectiles.append(self.currentPlayer.tank.shoot())  # Das vom Panzer geschossene Projektil wird zur Liste hinzugefügt
        self.nextPlayer()

    def nextPlayer(self):
        while True:
            self.currentPlayerNum = (self.currentPlayerNum+1) % self.playerCount
            if self.currentPlayer.inGame:
                break

    @property
    def currentPlayer(self):
        return self.players[self.currentPlayerNum]


if __name__ == "__main__":
    # Sets Logger to Debug
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    app = QApplication([])                                  # Öffnen der Anwendung
    app.setWindowIcon(QIcon('assets/images/player.gif'))    # Anwendungsicon
    artillary = Artillery(resolution = (800, 450), fullscreen = False)                                 # Öffnen des Fensters
    sys.exit(app.exec_())                                   # Schließung
