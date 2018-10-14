from gameObjects.particle import Particle
from gameObjects.projectile import Projectile
from tools.vector2 import Vector2
from PyQt5.QtCore import Qt
import numpy as np

# Ich bin mir nicht sicher ob der Aufbau aus 2 Partikeln so sinnvoll ist, das ganze macht die Koordinatenberechnung sehr schwer.
# bzw es wird ein Interface benötigt, dass die Arbeit mit 2 Partikeln verbirgt
# TODO: dringend! move so anpassen, dass die Unterseite auf dem Terrain aufliegt

class Tank:

    def __init__(self, positionX, positionY, terrain, speedX, color, sizeFactor = 4):
        """ Die Tank Klasse besteht aus zwei Partikeln, einem für den Körper und einem
            für den Lauf.
        """
        self.positionX = positionX
        self.positionY = positionY
        self.sizeFactor = sizeFactor                # bestimmt die Skalierung des Panzers
        self.bodyWidth = 13 * self.sizeFactor       # sollte ungerade bleiben
        self.bodyHeight = 6 * self.sizeFactor       # sollte gerade bleiben

        self.radius = 14 *self.sizeFactor

        self.rifleThickness = 1 * self.sizeFactor   # sollte ungerade bleiben
        self.rifleLength = 10 * self.sizeFactor     # sollte gerade bleiben
        self.body = Particle(positionX, positionY, self.bodyWidth, self.bodyHeight, 0, 0, color)

        self.rifleXOffset = - self.rifleThickness/2  #((((self.bodyWidth/self.rifleThickness)/2)-0.5) * self.rifleThickness)
        self.rifleYOffset = - self.rifleLength

        self.rifle = Particle(positionX + self.rifleXOffset, positionY + self.rifleYOffset
                              , self.rifleThickness, self.rifleLength, 0, 0, color)

        self.speedX = speedX                        # Fahrgeschwindigkeit des Panzers
        self.rotateSpeed = 4                        # Rotationsgeschwindigkeit des Lauf
        self.movingLeft = False
        self.movingRight = False
        self.movingRifleLeft = False
        self.movingRifleRight = False
        self.shooting = False  # wird gerade der Schuss geladen?
        self.rifleDegree = 90                       # Neigung des Laufs
        self.health = 100
        self.speedY = 0  # Für Stürze
        self.accelY = 0.5  # Für Stürze, könnte auch abhängig von Gewicht, oder Equipment wie Fallschirmen sein
        self.terrain = terrain  # wird benötigt zur Bewegung auf dem Terrain
        self.steigung = terrain.steigung(self.x)  # Steigung an der Stelle des Panzers, hieraus sollte auch Neigung berechnet werden

        self.powerBarMax = 100
        self.powerBarCurrent = 0
        self.powerBarUp = True

    def update(self):
        self.move()
        self.moveRifle()
        self.powerBar()
        
    def powerBar(self):
        if self.shooting:
            if self.powerBarUp:
                self.powerBarCurrent += 1
                if self.powerBarCurrent >= self.powerBarMax:
                    self.powerBarUp = False
            else:
                self.powerBarCurrent -= 1
                if self.powerBarCurrent <= 0:
                    self.powerBarUp = True
    
    def shoot(self):
        gegenkathete  = np.sin(np.deg2rad(self.rifleDegree)) * self.rifleLength + self.rifleThickness
        ankathete = np.cos(np.deg2rad(self.rifleDegree)) * self.rifleLength
        # Berechnet die Position des Projektils abhänging vom Lauf
        positionX = self.rifleX - ankathete
        positionY = self.rifleY + (self.rifleLength - gegenkathete)

        bulletspeed = self.powerBarCurrent/self.powerBarMax    # Stärke des Schusses

        self.powerBarUp = True
        self.shooting = False
        self.powerBarCurrent = 0

        return (Projectile(positionX,
                                              positionY,
                                              self.rifleThickness, self.rifleThickness,
                                              # Übergibt den Kraftvektor an das Geschoss
                                              -ankathete*bulletspeed,-gegenkathete*bulletspeed,
                                              Qt.gray))                 # Sollte anders gecodet sein
            
        
        

#  ich denke move sollte überarbeitet werden, mit einem generellen Geschwindigkeitsvektor
    def move(self):
        """ Die move Funktion überprüft erst ob das Bewegen des Panzers oder seines Laufs
            möglich ist und führt dann die Bewegung oder Rotation aus. Die Struktur ist wichtig,
            da die move Funktion in der Main Game Loop ständig aufgerufen wird. Durch das Drücken
            der Pfeiltasten verstellen sich dann die boolschen Variablen für die Bewegung und der Panzer
            bewegt sich. Durch diese Methode bewegt sich der Panzer sehr flüssig auf dem Bild. Eine
            Veränderung seiner Position durch Addition an seine momentane Position beim Drücken der Tasten
            ohne das move in der Main Game Loop hat sich als Ruckelig erwiesen.
        """
        if self.falling():
            self.speedY += self.accelY
            self.positionY += self.speedY
            if not self.falling():
                self.setYTerrainLevel()
                self.health -= self.speedY  # Lebensabzug bei Sturz (Abhängig von Tiefe/Geschwindigkeit)
                self.speedY = 0

        else:
            steigungsFaktor = abs(self.steigung)+1  # damit sich das Gefährt an der Steigung langsamer bewegt
            speed = self.speedX/steigungsFaktor  # man könnte einen mindestspeed einführen
            # speed gerät regelmäßig unter 1, was zu rucklern führt, weil dann nicht jedes Frame etwas geschieht
            # Todo: etwas anderes überlegen
            if self.movingLeft == True and self.movingRight == False:  # Bewegung nach links
                self.positionX -= speed
                if self.positionX < 1:  # verhindert verlassen der map
                    self.positionX = 1

            elif self.movingLeft == False and self.movingRight == True:  # Bewegung nach rechhts
                self.positionX += speed
                if self.positionX >= self.terrain.width - 2:  # verhindert verlassen der map
                    self.positionX = self.terrain.width - 2
            self.steigung = self.terrain.steigung(self.x)
            if self.diffToTerrainLevel()>-10:  # Y-Wert an Terrain anpassen (außer bei großen Stürzen)
                self.setYTerrainLevel()

    def moveRifle(self):# rifle
        if self.movingRifleLeft == True and self.movingRifleRight == False and self.rifleDegree > 0:
            self.rifleDegree -= self.rotateSpeed                    # Rotation gegen den Uhrzeigersinn
        elif self.movingRifleLeft == False and self.movingRifleRight == True and self.rifleDegree < 180:
            self.rifleDegree += self.rotateSpeed                    # Rotation mit dem Uhrzeigersinn

        self.updateComponentPosition()

    def updateComponentPosition(self):
        self.body.position.x = self.positionX
        self.body.position.y = self.positionY
        self.rifle.position.x = self.positionX + self.rifleXOffset
        self.rifle.position.y = self.positionY + self.rifleYOffset

    def falling(self):
        """gibt zurück, ob der Panzer sich gerade in der Luft befindet"""
        return self.positionY < self.terrain.surfaceY(self.x)

    def setYTerrainLevel(self):
        """setzt den Panzer an der aktuellen x Stelle genau auf die Höhe des Terrains"""
        self.positionY = self.terrain.surfaceY(self.x)


    def diffToTerrainLevel(self):
        """gibt den Abstand zum Terrain zurück"""
        return self.positionY-self.terrain.surfaceY(self.x)

    # muss dringedn überarbeitet werden.
    @property
    def x(self):
        return int(self.body.position.x)

    @property
    def y(self):
        return int(self.body.position.y)

    @property
    def rifleX(self):
        return int(self.rifle.position.x)

    @property
    def rifleY(self):
        return int(self.rifle.position.y)
