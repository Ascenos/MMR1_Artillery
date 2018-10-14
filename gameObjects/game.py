class Game(QLabel):
    """
    Die Game Klasse beschreibt das tatsächliche Spiel. Sie besitzt Listen
    mit Spielobjekten, einen Timer, einen Painter, berechnet den Verlauf
    des Spiels und gibt ihn wieder.
    """

    def __init__(self, parent, width, height, playerCount):
        """
        Initierung einfacher Variablen.
        """
        super().__init__(parent)

        self.width = width
        self.height = height
        self.playerCount = playerCount
        # Current player tracker
        self.currentPlayerNum = 0
        # Refresh rate in ms
        self.speed = 17

        self.initGame()

    def initGame(self):
        """
        Initierung der Spielobjekte, des Timers und anderer wichtiger
        Elemente.
        """
        # Set focus to QFrame to allow listening for the KeyPressEvent
        self.setFocusPolicy(Qt.StrongFocus)
        self.terrain = Terrain(self.width, self.height)
        self.terrain.generateByFourierSynthesis()
        self.terrain.generateQImage()
        self.particles = []
        self.projectiles = []
        self.players = []
        # TODO implement this as GUI input
        players = [("Amadeus", Qt.red), ("Jannik", Qt.green), ("Mario", Qt.blue)]
        for num, (name, color) in enumerate(players):
            tank = Tank((num+1)*self.width/(len(players)+1),500,self.terrain,2,color)
            self.players.append(Player(name, tank))
        # Create game timer
        self.timer = QBasicTimer()

    def start(self):
        """
        Start des Spiels.
        """
        # Start timer
        self.timer.start(self.speed, self)

    def paintEvent(self, QPaintEvent):
        """
        Generiert einen Painter und gibt ihm die Anweisung das Spiel
        zu zeichnen.
        """

        painter = QPainter(self)
        # Draw game elements
        self.drawGame(painter)
        painter.end()

    def drawGame(self, painter):
        """
        Zeichnet alle Spielgegenstände.
        """
        self.drawBackground(painter)
        self.terrain.drawImage(painter)
        self.drawStatus(painter)
        self.drawParticles(painter)
        self.drawProjectile(painter)
        self.drawTanks(painter)


    def drawBackground(self, painter):
        """
        Zeichnet den Hintergrund.
        """
        painter.fillRect(0,0, self.width, self.height, QColor(200,220,255))

    def drawParticles(self, painter):
        """
        Anweisung zum Zeichnen von Rechteckigen Partikeln.
        """
        for particle in self.particles:
            painter.fillRect(particle.position.x, particle.position.y, particle.size.x, particle.size.y, particle.color)

    def drawTanks(self, painter):
        """ Anweisung zum Zeichnen von Panzern."""
        for player in self.players:
            # Exclude players that are not in game anymore
            if not player.inGame:
                continue
            # Draw actual tanks
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
        """
        Zeichnet alle Projektiele.
        """
        for projectile in self.projectiles:
            painter.fillRect(projectile.position.x, projectile.position.y, projectile.size.x, projectile.size.y, projectile.color)

    def timerEvent(self, QTimerEvent):
        """
        Die Haupt-Spiel-Schleife (Main Game Loop).
        """
        for particle in self.particles:
            particle.move()
        for player in self.players:
            player.tank.update()
        for projectile in self.projectiles:
            projectile.move()
        self.update()
# Zeichnet das Bild neu


    def keyPressEvent(self, QKeyEvent):
        """
        Der Eventhandler für gedrückte Tasten
        """
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
        """
        Der Eventhandler für losgelassene Tasten
        """
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
        """
        Schießt ein Projektil aus dem Lauf des aktuellen Panzers
        """
        # Append tank projectile to projectiles list
        self.projectiles.append(self.currentPlayer.tank.shoot())
        self.nextPlayer()

    def nextPlayer(self):
        """
        Find next Player in the row.
        """
        while True:
            self.currentPlayerNum = (self.currentPlayerNum+1) % self.playerCount
            if self.currentPlayer.inGame:
                break

    @property
    def currentPlayer(self):
        return self.players[self.currentPlayerNum]